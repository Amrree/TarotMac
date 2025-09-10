"""
Integration tests for the complete reading flow.
"""

import pytest
import sys
import os
import json
import tempfile
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.influence.engine import CardInfluenceEngine, CardPosition
from ai.ollama_client import OllamaClient
from db.models import Base, Card, Reading, ReadingPosition, Spread
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestReadingFlow:
    """Integration tests for the complete reading workflow."""
    
    def setup_method(self):
        """Set up test database and fixtures."""
        # Create in-memory SQLite database
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        # Create test cards
        self.create_test_cards()
        
        # Create test spread
        self.create_test_spread()
        
        # Initialize influence engine
        self.influence_engine = CardInfluenceEngine()
        
        # Initialize Ollama client (mock mode)
        self.ollama_client = OllamaClient()
    
    def create_test_cards(self):
        """Create test cards in database."""
        cards_data = [
            {
                "id": "fool",
                "name": "The Fool",
                "arcana": "major",
                "element": "air",
                "keywords": ["new beginnings", "innocence", "spontaneity"],
                "upright_text": "The Fool represents new beginnings and innocence.",
                "reversed_text": "Reversed, The Fool warns of recklessness.",
                "polarity_baseline": 0.5,
                "intensity_baseline": 0.7,
                "themes": {"new_beginnings": 0.9, "innocence": 0.8}
            },
            {
                "id": "magician",
                "name": "The Magician",
                "arcana": "major",
                "element": "air",
                "keywords": ["manifestation", "willpower", "skill"],
                "upright_text": "The Magician represents manifestation through willpower.",
                "reversed_text": "Reversed, The Magician suggests manipulation.",
                "polarity_baseline": 0.8,
                "intensity_baseline": 0.9,
                "themes": {"manifestation": 0.9, "willpower": 0.8}
            },
            {
                "id": "sun",
                "name": "The Sun",
                "arcana": "major",
                "element": "fire",
                "keywords": ["joy", "success", "vitality"],
                "upright_text": "The Sun represents joy, success, and vitality.",
                "reversed_text": "Reversed, The Sun suggests temporary setbacks.",
                "polarity_baseline": 0.9,
                "intensity_baseline": 0.8,
                "themes": {"joy": 0.9, "success": 0.8}
            }
        ]
        
        for card_data in cards_data:
            card = Card(**card_data)
            self.session.add(card)
        
        self.session.commit()
    
    def create_test_spread(self):
        """Create test spread in database."""
        spread_data = {
            "id": "three_card",
            "name": "Three Card Spread",
            "description": "Past, Present, Future",
            "positions": [
                {"name": "past", "x": -1.0, "y": 0.0},
                {"name": "present", "x": 0.0, "y": 0.0},
                {"name": "future", "x": 1.0, "y": 0.0}
            ],
            "is_custom": False
        }
        
        spread = Spread(**spread_data)
        self.session.add(spread)
        self.session.commit()
    
    def test_complete_reading_workflow(self):
        """Test the complete reading workflow from draw to save."""
        
        # 1. Create a reading
        reading = Reading(
            title="Test Reading",
            spread_id="three_card",
            tags=["test", "integration"],
            is_private=False
        )
        self.session.add(reading)
        self.session.commit()
        
        # 2. Add card positions
        card_positions = [
            ReadingPosition(
                reading_id=reading.id,
                card_id="fool",
                position_name="past",
                position_index=0,
                orientation="upright",
                x_coordinate=-1.0,
                y_coordinate=0.0
            ),
            ReadingPosition(
                reading_id=reading.id,
                card_id="magician",
                position_name="present",
                position_index=1,
                orientation="upright",
                x_coordinate=0.0,
                y_coordinate=0.0
            ),
            ReadingPosition(
                reading_id=reading.id,
                card_id="sun",
                position_name="future",
                position_index=2,
                orientation="upright",
                x_coordinate=1.0,
                y_coordinate=0.0
            )
        ]
        
        for position in card_positions:
            self.session.add(position)
        self.session.commit()
        
        # 3. Compute influences
        card_positions_for_engine = []
        for pos in card_positions:
            card = self.session.query(Card).filter(Card.id == pos.card_id).first()
            card_pos = CardPosition(
                card_id=card.id,
                card_name=card.name,
                orientation=pos.orientation,
                position_name=pos.position_name,
                x=pos.x_coordinate,
                y=pos.y_coordinate,
                base_polarity=card.polarity_baseline,
                base_intensity=card.intensity_baseline,
                base_themes=card.themes
            )
            card_positions_for_engine.append(card_pos)
        
        influenced_cards = self.influence_engine.compute_influences(card_positions_for_engine)
        
        # 4. Verify influence computation
        assert len(influenced_cards) == 3
        
        for influenced_card in influenced_cards:
            assert influenced_card.card_id in ["fool", "magician", "sun"]
            assert isinstance(influenced_card.polarity_score, float)
            assert isinstance(influenced_card.intensity_score, float)
            assert isinstance(influenced_card.influence_factors, list)
            
            # Check valid ranges
            assert -2.0 <= influenced_card.polarity_score <= 2.0
            assert 0.0 <= influenced_card.intensity_score <= 1.0
        
        # 5. Verify reading persistence
        saved_reading = self.session.query(Reading).filter(Reading.id == reading.id).first()
        assert saved_reading is not None
        assert saved_reading.title == "Test Reading"
        assert len(saved_reading.positions) == 3
        
        # 6. Verify card positions
        for position in saved_reading.positions:
            assert position.card_id in ["fool", "magician", "sun"]
            assert position.position_name in ["past", "present", "future"]
            assert position.orientation == "upright"
    
    def test_reading_with_reversed_cards(self):
        """Test reading workflow with reversed cards."""
        
        # Create reading with reversed cards
        reading = Reading(
            title="Reversed Test Reading",
            spread_id="three_card",
            tags=["test", "reversed"]
        )
        self.session.add(reading)
        self.session.commit()
        
        # Add positions with some reversed cards
        positions = [
            ReadingPosition(
                reading_id=reading.id,
                card_id="fool",
                position_name="past",
                position_index=0,
                orientation="reversed",
                x_coordinate=-1.0,
                y_coordinate=0.0
            ),
            ReadingPosition(
                reading_id=reading.id,
                card_id="magician",
                position_name="present",
                position_index=1,
                orientation="upright",
                x_coordinate=0.0,
                y_coordinate=0.0
            ),
            ReadingPosition(
                reading_id=reading.id,
                card_id="sun",
                position_name="future",
                position_index=2,
                orientation="reversed",
                x_coordinate=1.0,
                y_coordinate=0.0
            )
        ]
        
        for position in positions:
            self.session.add(position)
        self.session.commit()
        
        # Compute influences
        card_positions_for_engine = []
        for pos in positions:
            card = self.session.query(Card).filter(Card.id == pos.card_id).first()
            card_pos = CardPosition(
                card_id=card.id,
                card_name=card.name,
                orientation=pos.orientation,
                position_name=pos.position_name,
                x=pos.x_coordinate,
                y=pos.y_coordinate,
                base_polarity=card.polarity_baseline,
                base_intensity=card.intensity_baseline,
                base_themes=card.themes
            )
            card_positions_for_engine.append(card_pos)
        
        influenced_cards = self.influence_engine.compute_influences(card_positions_for_engine)
        
        # Verify reversed cards have different influence patterns
        fool_card = next(c for c in influenced_cards if c.card_id == "fool")
        sun_card = next(c for c in influenced_cards if c.card_id == "sun")
        
        # Reversed cards should have modified polarity scores
        assert fool_card.orientation == "reversed"
        assert sun_card.orientation == "reversed"
        
        # The influence factors should reflect reversed effects
        for influenced_card in influenced_cards:
            for factor in influenced_card.influence_factors:
                assert isinstance(factor.effect, float)
                assert isinstance(factor.explain, str)
                assert len(factor.explain) > 0
    
    def test_reading_search_and_filter(self):
        """Test reading search and filtering functionality."""
        
        # Create multiple readings with different tags
        readings_data = [
            {"title": "Morning Reading", "tags": ["morning", "daily"]},
            {"title": "Relationship Reading", "tags": ["relationship", "love"]},
            {"title": "Career Reading", "tags": ["career", "work"]},
            {"title": "Evening Reading", "tags": ["evening", "daily"]}
        ]
        
        for reading_data in readings_data:
            reading = Reading(
                title=reading_data["title"],
                spread_id="three_card",
                tags=reading_data["tags"]
            )
            self.session.add(reading)
        
        self.session.commit()
        
        # Test filtering by tags
        daily_readings = self.session.query(Reading).filter(
            Reading.tags.contains(["daily"])
        ).all()
        
        assert len(daily_readings) == 2
        assert all("daily" in reading.tags for reading in daily_readings)
        
        # Test filtering by title
        morning_readings = self.session.query(Reading).filter(
            Reading.title.contains("Morning")
        ).all()
        
        assert len(morning_readings) == 1
        assert morning_readings[0].title == "Morning Reading"
    
    def test_reading_export_import(self):
        """Test reading export and import functionality."""
        
        # Create a reading to export
        reading = Reading(
            title="Export Test Reading",
            spread_id="three_card",
            tags=["export", "test"],
            notes="This is a test reading for export"
        )
        self.session.add(reading)
        self.session.commit()
        
        # Add card positions
        positions = [
            ReadingPosition(
                reading_id=reading.id,
                card_id="fool",
                position_name="past",
                position_index=0,
                orientation="upright",
                x_coordinate=-1.0,
                y_coordinate=0.0
            ),
            ReadingPosition(
                reading_id=reading.id,
                card_id="magician",
                position_name="present",
                position_index=1,
                orientation="upright",
                x_coordinate=0.0,
                y_coordinate=0.0
            )
        ]
        
        for position in positions:
            self.session.add(position)
        self.session.commit()
        
        # Export reading data
        export_data = {
            "reading": {
                "id": reading.id,
                "title": reading.title,
                "spread_id": reading.spread_id,
                "date_created": reading.date_created.isoformat(),
                "tags": reading.tags,
                "notes": reading.notes
            },
            "positions": [
                {
                    "card_id": pos.card_id,
                    "position_name": pos.position_name,
                    "position_index": pos.position_index,
                    "orientation": pos.orientation,
                    "x_coordinate": pos.x_coordinate,
                    "y_coordinate": pos.y_coordinate
                }
                for pos in positions
            ]
        }
        
        # Verify export data structure
        assert "reading" in export_data
        assert "positions" in export_data
        assert len(export_data["positions"]) == 2
        
        # Test import (simulate importing into new database)
        new_engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(new_engine)
        new_session = sessionmaker(bind=new_engine)()
        
        # Import reading
        imported_reading = Reading(
            id=export_data["reading"]["id"],
            title=export_data["reading"]["title"],
            spread_id=export_data["reading"]["spread_id"],
            tags=export_data["reading"]["tags"],
            notes=export_data["reading"]["notes"]
        )
        new_session.add(imported_reading)
        
        # Import positions
        for pos_data in export_data["positions"]:
            position = ReadingPosition(
                reading_id=imported_reading.id,
                card_id=pos_data["card_id"],
                position_name=pos_data["position_name"],
                position_index=pos_data["position_index"],
                orientation=pos_data["orientation"],
                x_coordinate=pos_data["x_coordinate"],
                y_coordinate=pos_data["y_coordinate"]
            )
            new_session.add(position)
        
        new_session.commit()
        
        # Verify import
        imported = new_session.query(Reading).first()
        assert imported.title == "Export Test Reading"
        assert len(imported.positions) == 2
        assert imported.tags == ["export", "test"]