# Tarot Influence Engine Design Document

## Overview

The Tarot Influence Engine is a deterministic system that computes how neighboring cards modify each other's meanings within a tarot spread. The engine applies established tarot combination methods through algorithmic rules, producing structured, explainable interpretations with traceable influence factors.

## Design Principles

### 1. Deterministic Behavior
- Same input spread + rules = same output
- All influence calculations are mathematically traceable
- No randomness or subjective interpretation in core algorithms

### 2. Explainable Results
- Every influence factor must have a clear source and explanation
- Influence calculations are logged with specific rule applications
- Confidence levels indicate certainty of interpretations

### 3. Configurable Rules
- All influence rules can be enabled/disabled
- Rule parameters can be adjusted (multipliers, thresholds)
- Support for custom rule overrides per deck or user

### 4. Fallback Capability
- Engine must work without external LLM dependencies
- Template-based text generation for influenced meanings
- Graceful degradation when advanced features unavailable

## Data Model

### Card Schema
```json
{
  "card_id": "string",
  "name": "string",
  "arcana": "major|minor",
  "suit": "wands|cups|swords|pentacles|null",
  "number": "integer|null",
  "rank": "page|knight|queen|king|null",
  "element": "fire|water|air|earth",
  "baseline_polarity": "float (-1.0 to +1.0)",
  "baseline_intensity": "float (0.0 to 1.0)",
  "keywords": ["string"],
  "base_upright_text": "string",
  "base_reversed_text": "string",
  "themes": {
    "theme_name": "float (0.0 to 1.0)"
  }
}
```

### Spread Schema
```json
{
  "reading_id": "string",
  "date_time": "ISO8601 string",
  "spread_type": "string",
  "positions": [
    {
      "position_id": "string",
      "card_id": "string",
      "orientation": "upright|reversed",
      "x_coordinate": "float",
      "y_coordinate": "float"
    }
  ],
  "user_context": "string|null"
}
```

### Influence Vector Schema
```json
{
  "polarity": "float (-2.0 to +2.0)",
  "intensity": "float (0.0 to 1.0)",
  "themes": {
    "theme_name": "float (0.0 to 1.0)"
  }
}
```

### Influence Factor Schema
```json
{
  "source_position": "string",
  "source_card_id": "string",
  "effect": "float",
  "explain": "string",
  "confidence": "high|medium|low"
}
```

## Adjacency Strategy

### Distance-Based Weighting
The engine uses Euclidean distance between card positions to determine adjacency weights:

```python
def calculate_adjacency_weight(pos1, pos2):
    distance = sqrt((pos1.x - pos2.x)**2 + (pos1.y - pos2.y)**2)
    
    if distance <= 1.0:
        return 1.0      # Direct adjacency
    elif distance <= 1.5:
        return 0.7      # Diagonal adjacency
    elif distance <= 2.5:
        return 0.5      # Same row/column
    elif distance <= 4.0:
        return 0.3      # Nearby
    else:
        return 0.1      # Distant
```

### Standard Spread Adjacency Tables

#### Three-Card Spread (Past-Present-Future)
```
Position 1 (Past)    Position 2 (Present)    Position 3 (Future)
     (0,0)                (1,0)                  (2,0)

Adjacency Matrix:
        1    2    3
    1  -   1.0  0.0
    2  1.0  -   1.0
    3  0.0 1.0   -
```

#### Celtic Cross Spread
```
Position 1 (Center)     Position 2 (Cross)
     (0,0)                   (1,0)
Position 3 (Past)       Position 4 (Future)
     (0,1)                   (1,1)
Position 5 (Above)      Position 6 (Below)
     (0,2)                   (1,2)
Position 7 (Self)       Position 8 (Environment)
     (2,0)                   (2,1)
Position 9 (Hopes)      Position 10 (Outcome)
     (2,2)                   (2,3)

Adjacency weights calculated dynamically based on distance.
```

## Rule Pipeline

### Stage 1: Major Arcana Dominance
**Priority**: Highest
**Function**: Apply Major Arcana influence multipliers
**Rules**:
- Major Arcana cards receive 1.5x influence multiplier
- Multiple Majors create cumulative dominance
- Major Arcana can override minor suit tendencies

**Implementation**:
```python
def apply_major_dominance(card, neighbors):
    if card.arcana == "major":
        for neighbor in neighbors:
            influence_weight = adjacency_weight * 1.5
            neighbor.influence_multiplier *= influence_weight
```

### Stage 2: Adjacency Accumulation
**Priority**: High
**Function**: Apply proximity-based influence
**Rules**:
- Direct adjacency: 100% influence weight
- Diagonal adjacency: 70% influence weight
- Same row/column: 50% influence weight
- Distant positions: 20% influence weight

**Implementation**:
```python
def apply_adjacency_influence(card, neighbors):
    for neighbor in neighbors:
        weight = calculate_adjacency_weight(card.position, neighbor.position)
        influence = weight * neighbor.baseline_polarity
        card.polarity_effect += influence
```

### Stage 3: Elemental Adjustments
**Priority**: Medium
**Function**: Apply elemental dignity rules
**Rules**:
- Same elements: +20% theme reinforcement
- Complementary elements: +10% theme enhancement
- Opposing elements: -15% conflicting themes

**Implementation**:
```python
def apply_elemental_dignities(card, neighbors):
    for neighbor in neighbors:
        if card.element == neighbor.element:
            # Same element reinforcement
            card.theme_boost += 0.2
        elif is_complementary(card.element, neighbor.element):
            # Complementary enhancement
            card.theme_boost += 0.1
        elif is_opposing(card.element, neighbor.element):
            # Opposing element tension
            card.theme_reduction += 0.15
```

### Stage 4: Numerical Sequence Adjustments
**Priority**: Medium
**Function**: Detect and apply numerical patterns
**Rules**:
- Ascending sequences: +15% continuity themes
- Descending sequences: +15% completion themes
- Same numbers: +20% thematic emphasis
- Broken sequences: -10% continuity themes

**Implementation**:
```python
def apply_numerical_sequences(cards):
    sequences = detect_sequences(cards)
    for sequence in sequences:
        if sequence.type == "ascending":
            for card in sequence.cards:
                card.continuity_boost += 0.15
        elif sequence.type == "descending":
            for card in sequence.cards:
                card.completion_boost += 0.15
```

### Stage 5: Suit Predominance
**Priority**: Medium
**Function**: Apply suit-based theme emphasis
**Rules**:
- 3+ same suit: +25% suit themes, -15% opposing themes
- 4+ same suit: +35% suit themes, -25% opposing themes
- 2+ same suit: +10% suit themes
- Mixed suits: balanced theme distribution

**Implementation**:
```python
def apply_suit_predominance(cards):
    suit_counts = count_suits(cards)
    for suit, count in suit_counts.items():
        if count >= 3:
            theme_boost = 0.25 if count == 3 else 0.35
            for card in cards:
                if card.suit == suit:
                    card.suit_theme_boost += theme_boost
                else:
                    card.opposing_theme_reduction += 0.15
```

### Stage 6: Reversal Propagation
**Priority**: Medium
**Function**: Apply reversal effects to neighboring cards
**Rules**:
- Reversed cards: -30% stability themes in neighbors
- Multiple reversed cards: cumulative effect
- Reversed Majors: stronger reversal propagation

**Implementation**:
```python
def apply_reversal_propagation(card, neighbors):
    if card.orientation == "reversed":
        reversal_strength = 0.3
        if card.arcana == "major":
            reversal_strength *= 1.5
        
        for neighbor in neighbors:
            neighbor.stability_reduction += reversal_strength
```

### Stage 7: Conflict Resolution
**Priority**: Low
**Function**: Resolve conflicting influences
**Rules**:
- Strong opposing polarities: mutual dampening
- Conflicting themes: weighted resolution
- Multiple influences: weighted average

**Implementation**:
```python
def resolve_conflicts(card):
    # Apply weighted average for conflicting influences
    if abs(card.positive_influence - card.negative_influence) > 0.5:
        # Strong conflict - apply dampening
        card.conflict_dampening = 0.7
        card.final_polarity *= card.conflict_dampening
```

### Stage 8: Normalization
**Priority**: Low
**Function**: Ensure all values are within valid ranges
**Rules**:
- Polarity: clamp to [-2.0, +2.0]
- Intensity: clamp to [0.0, 1.0]
- Themes: clamp to [0.0, 1.0]

**Implementation**:
```python
def normalize_scores(card):
    card.polarity_score = clamp(card.polarity_score, -2.0, 2.0)
    card.intensity_score = clamp(card.intensity_score, 0.0, 1.0)
    for theme, weight in card.themes.items():
        card.themes[theme] = clamp(weight, 0.0, 1.0)
```

### Stage 9: Theme Aggregation
**Priority**: Low
**Function**: Combine and weight theme influences
**Rules**:
- Sum all theme influences
- Apply narrative boosting for shared themes
- Weight themes by intensity

**Implementation**:
```python
def aggregate_themes(card, all_cards):
    # Apply narrative boosting for shared themes
    shared_themes = find_shared_themes(card, all_cards)
    for theme in shared_themes:
        card.themes[theme] *= 1.2  # 20% boost for shared themes
```

## Configuration Options

### Rule Configuration
```json
{
  "major_dominance": {
    "enabled": true,
    "multiplier": 1.5,
    "override_threshold": 0.7
  },
  "adjacency_weighting": {
    "enabled": true,
    "distance_decay": 0.8,
    "max_distance": 4.0
  },
  "elemental_dignities": {
    "enabled": true,
    "same_element_boost": 0.2,
    "complementary_boost": 0.1,
    "opposing_reduction": 0.15
  },
  "numerical_sequences": {
    "enabled": true,
    "ascending_boost": 0.15,
    "descending_boost": 0.15,
    "same_number_boost": 0.2
  },
  "suit_predominance": {
    "enabled": true,
    "three_card_boost": 0.25,
    "four_card_boost": 0.35,
    "opposing_reduction": 0.15
  },
  "reversal_propagation": {
    "enabled": true,
    "stability_reduction": 0.3,
    "major_multiplier": 1.5
  }
}
```

### Spread Configuration
```json
{
  "spread_types": {
    "three_card": {
      "positions": [
        {"id": "past", "x": 0, "y": 0},
        {"id": "present", "x": 1, "y": 0},
        {"id": "future", "x": 2, "y": 0}
      ]
    },
    "celtic_cross": {
      "positions": [
        {"id": "center", "x": 0, "y": 0},
        {"id": "cross", "x": 1, "y": 0},
        {"id": "past", "x": 0, "y": 1},
        {"id": "future", "x": 1, "y": 1},
        {"id": "above", "x": 0, "y": 2},
        {"id": "below", "x": 1, "y": 2},
        {"id": "self", "x": 2, "y": 0},
        {"id": "environment", "x": 2, "y": 1},
        {"id": "hopes", "x": 2, "y": 2},
        {"id": "outcome", "x": 2, "y": 3}
      ]
    }
  }
}
```

## API Contract

### Input Schema
```json
{
  "reading_id": "string",
  "date_time": "ISO8601 string",
  "spread_type": "string",
  "positions": [
    {
      "position_id": "string",
      "card_id": "string",
      "orientation": "upright|reversed",
      "x_coordinate": "float",
      "y_coordinate": "float"
    }
  ],
  "user_context": "string|null",
  "rule_overrides": "object|null"
}
```

### Output Schema
```json
{
  "reading_id": "string",
  "summary": "string",
  "cards": [
    {
      "position": "string",
      "card_id": "string",
      "card_name": "string",
      "orientation": "upright|reversed",
      "base_text": "string",
      "influenced_text": "string",
      "polarity_score": "float",
      "intensity_score": "float",
      "themes": {
        "theme_name": "float"
      },
      "influence_factors": [
        {
          "source_position": "string",
          "source_card_id": "string",
          "effect": "float",
          "explain": "string",
          "confidence": "high|medium|low"
        }
      ],
      "journal_prompt": "string"
    }
  ],
  "advice": ["string"],
  "follow_up_questions": ["string"]
}
```

## Natural Language Generation

### Template-Based Generation
When LLM is unavailable, the engine uses deterministic templates:

```python
def generate_influenced_text(card, influence_factors):
    base_text = card.base_reversed_text if card.orientation == "reversed" else card.base_upright_text
    
    if influence_factors:
        influences = []
        for factor in influence_factors:
            if factor.effect > 0.3:
                influences.append(f"enhanced by {factor.source_card_name}")
            elif factor.effect < -0.3:
                influences.append(f"tempered by {factor.source_card_name}")
        
        if influences:
            influenced_text = f"{base_text} This meaning is {', '.join(influences)}."
        else:
            influenced_text = base_text
    else:
        influenced_text = base_text
    
    return influenced_text
```

### LLM Integration
When LLM is available, the engine provides structured context:

```python
def generate_llm_prompt(card, influence_factors):
    prompt = f"""
    Generate influenced interpretation for {card.name} ({card.orientation}):
    
    Base meaning: {card.base_text}
    Polarity score: {card.polarity_score}
    Intensity score: {card.intensity_score}
    
    Influence factors:
    """
    
    for factor in influence_factors:
        prompt += f"- {factor.source_card_name}: {factor.effect:+.2f} ({factor.explain})\n"
    
    prompt += """
    Return JSON with influenced_text and journal_prompt fields.
    """
    
    return prompt
```

## Error Handling

### Validation
- Input schema validation
- Card ID validation against deck
- Position coordinate validation
- Rule parameter validation

### Fallbacks
- Missing card data: use default values
- Invalid positions: use center position (0,0)
- Rule errors: disable problematic rule
- LLM unavailable: use template generation

### Logging
- All rule applications logged with parameters
- Influence calculations logged with intermediate values
- Error conditions logged with context
- Performance metrics logged for optimization

## Performance Considerations

### Optimization Strategies
- Pre-compute adjacency matrices for standard spreads
- Cache elemental correspondence lookups
- Batch process theme calculations
- Use efficient data structures for influence tracking

### Scalability
- Engine designed to handle spreads up to 20 cards
- Memory usage scales linearly with card count
- Processing time scales quadratically with card count
- Configurable limits for large spreads

## Testing Strategy

### Unit Tests
- Individual rule testing with known inputs
- Edge case coverage for each rule
- Boundary condition testing
- Error condition testing

### Integration Tests
- Complete spread processing
- Multiple rule interaction testing
- Schema validation testing
- Performance benchmarking

### Validation Tests
- Output schema compliance
- Deterministic behavior verification
- Influence factor traceability
- Confidence scoring accuracy

## Implementation Notes

### Data Storage
- Cards stored in SQLite database
- Influence calculations stored in memory
- Rule configurations stored in JSON files
- Spread definitions stored in configuration files

### Threading
- Engine designed for single-threaded operation
- No shared state between calculations
- Thread-safe for concurrent reading processing
- Async support for LLM integration

### Extensibility
- Plugin architecture for custom rules
- Configuration-driven rule parameters
- Support for custom spread types
- Extensible theme system

This design provides a comprehensive foundation for implementing a deterministic, explainable tarot influence engine that can systematically apply established practitioner methods while maintaining the flexibility and depth of traditional tarot interpretation.