"""
History manager for integrating GUI with history module.
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

# Import history module
from history.reading_storage import ReadingStorage
from history.search_filter import SearchFilter

logger = logging.getLogger(__name__)


class HistoryManager:
    """Manages reading history and integrates with GUI."""
    
    def __init__(self):
        """Initialize the history manager."""
        self.storage = ReadingStorage()
        self.search_filter = SearchFilter()
        
        # Current search state
        self.current_search_results = []
        self.current_filter = None
    
    def saveReading(self, reading_data: Dict[str, Any]) -> bool:
        """Save a reading to history."""
        try:
            # Add timestamp if not present
            if 'timestamp' not in reading_data:
                reading_data['timestamp'] = datetime.now().isoformat()
            
            # Save to storage
            success = self.storage.save_reading(reading_data)
            if success:
                logger.info(f"Saved reading: {reading_data.get('id', 'unknown')}")
                return True
            else:
                logger.error("Failed to save reading")
                return False
                
        except Exception as e:
            logger.error(f"Error saving reading: {e}")
            return False
    
    def getAllReadings(self) -> List[Dict[str, Any]]:
        """Get all saved readings."""
        try:
            readings = self.storage.get_all_readings()
            logger.info(f"Retrieved {len(readings)} readings")
            return readings
        except Exception as e:
            logger.error(f"Error getting readings: {e}")
            return []
    
    def searchReadings(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search readings with optional filters."""
        try:
            # Get all readings first
            all_readings = self.getAllReadings()
            
            # Apply search filter
            if query:
                results = self.search_filter.search(all_readings, query)
            else:
                results = all_readings
            
            # Apply additional filters
            if filters:
                results = self.search_filter.filter_by_criteria(results, filters)
            
            self.current_search_results = results
            self.current_filter = filters
            
            logger.info(f"Search returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error searching readings: {e}")
            return []
    
    def getReadingById(self, reading_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific reading by ID."""
        try:
            reading = self.storage.get_reading_by_id(reading_id)
            if reading:
                logger.info(f"Retrieved reading: {reading_id}")
                return reading
            else:
                logger.warning(f"Reading not found: {reading_id}")
                return None
        except Exception as e:
            logger.error(f"Error getting reading {reading_id}: {e}")
            return None
    
    def deleteReading(self, reading_id: str) -> bool:
        """Delete a reading from history."""
        try:
            success = self.storage.delete_reading(reading_id)
            if success:
                logger.info(f"Deleted reading: {reading_id}")
                return True
            else:
                logger.error(f"Failed to delete reading: {reading_id}")
                return False
        except Exception as e:
            logger.error(f"Error deleting reading {reading_id}: {e}")
            return False
    
    def exportReadings(self, file_path: str, format: str = 'json') -> bool:
        """Export readings to a file."""
        try:
            readings = self.getAllReadings()
            success = self.storage.export_readings(readings, file_path, format)
            if success:
                logger.info(f"Exported {len(readings)} readings to {file_path}")
                return True
            else:
                logger.error(f"Failed to export readings to {file_path}")
                return False
        except Exception as e:
            logger.error(f"Error exporting readings: {e}")
            return False
    
    def importReadings(self, file_path: str, format: str = 'json') -> bool:
        """Import readings from a file."""
        try:
            success = self.storage.import_readings(file_path, format)
            if success:
                logger.info(f"Imported readings from {file_path}")
                return True
            else:
                logger.error(f"Failed to import readings from {file_path}")
                return False
        except Exception as e:
            logger.error(f"Error importing readings: {e}")
            return False
    
    def getSearchResults(self) -> List[Dict[str, Any]]:
        """Get current search results."""
        return self.current_search_results
    
    def getCurrentFilter(self) -> Optional[Dict[str, Any]]:
        """Get current search filter."""
        return self.current_filter
    
    def clearSearch(self):
        """Clear current search results."""
        self.current_search_results = []
        self.current_filter = None
        logger.info("Cleared search results")