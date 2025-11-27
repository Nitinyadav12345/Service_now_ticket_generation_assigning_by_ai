# Capacity Calculation Configuration

## Formula

The system uses the industry-standard sprint capacity formula:

```
Sprint Capacity = (Working Days × Daily Working Hours − Leave Hours) × Focus Factor
Story Points = Available Hours / Hours Per Story Point
```

## Configuration Parameters

Add these to your `Backend/.env` file:

```env
# Capacity Calculation Settings
DAILY_WORKING_HOURS=8          # Hours per work day
HOURS_PER_STORY_POINT=4.0      # Hours needed per story point
FOCUS_FACTOR=0.7               # Focus factor (0.0 to 1.0)
```

## Parameter Details

### Daily Working Hours
- **Default**: 8 hours
- **Description**: Standard working hours per day
- **Typical Values**: 6-8 hours
- **Example**: `DAILY_WORKING_HOURS=8`

### Hours Per Story Point
- **Default**: 4.0 hours
- **Description**: Average hours needed to complete 1 story point
- **Typical Values**: 2-6 hours
- **Calibration**: 
  - 2 hours = Very small tasks
  - 4 hours = Standard (half day)
  - 6 hours = Larger tasks
- **Example**: `HOURS_PER_STORY_POINT=4.0`

### Focus Factor
- **Default**: 0.7 (70%)
- **Description**: Percentage of time actually spent on development
- **Accounts For**:
  - Meetings
  - Emails
  - Code reviews
  - Context switching
  - Breaks
  - Administrative tasks
- **Typical Values**:
  - 0.5-0.6 (50-60%): Heavy meeting culture
  - 0.7 (70%): Balanced team (recommended)
  - 0.8-0.9 (80-90%): Highly focused team
- **Example**: `FOCUS_FACTOR=0.7`

## Calculation Examples

### Example 1: Standard 2-Week Sprint
```
Sprint Duration: 14 days
Working Days: (14 / 7) × 5 = 10 days
Daily Hours: 8 hours
Leave Hours: 0 hours
Focus Factor: 0.7

Available Hours = (10 × 8 − 0) × 0.7 = 56 hours
Story Points = 56 / 4 = 14 points
```

### Example 2: With Leave
```
Sprint Duration: 14 days
Working Days: 10 days
Daily Hours: 8 hours
Leave Hours: 16 hours (2 days off)
Focus Factor: 0.7

Available Hours = (10 × 8 − 16) × 0.7 = 44.8 hours
Story Points = 44.8 / 4 = 11 points
```

### Example 3: Part-Time Developer
```
Sprint Duration: 14 days
Working Days: 10 days
Daily Hours: 4 hours (part-time)
Leave Hours: 0 hours
Focus Factor: 0.7

Available Hours = (10 × 4 − 0) × 0.7 = 28 hours
Story Points = 28 / 4 = 7 points
```

## Calibration Guide

### Step 1: Measure Historical Velocity
1. Look at last 3 sprints
2. Calculate average story points completed per developer
3. This is your baseline

### Step 2: Adjust Hours Per Story Point
```
Hours Per Story Point = (Working Days × Daily Hours × Focus Factor) / Average Story Points
```

Example:
- 10 working days × 8 hours × 0.7 = 56 hours
- Average completed: 12 points
- Hours per point = 56 / 12 = 4.67 hours

### Step 3: Fine-Tune Focus Factor
If developers consistently:
- **Over-commit**: Increase focus factor (0.75-0.8)
- **Under-commit**: Decrease focus factor (0.6-0.65)

### Step 4: Monitor and Adjust
- Review every 2-3 sprints
- Adjust based on actual completion rates
- Consider team feedback

## Team-Specific Adjustments

### Junior Developers
```env
HOURS_PER_STORY_POINT=6.0    # Need more time per point
FOCUS_FACTOR=0.6             # More learning/mentoring time
```

### Senior Developers
```env
HOURS_PER_STORY_POINT=3.0    # Faster completion
FOCUS_FACTOR=0.65            # More meetings/mentoring
```

### DevOps/Platform Teams
```env
FOCUS_FACTOR=0.5             # More interruptions/incidents
```

## Status Thresholds

Based on calculated capacity:

- **Available**: < 75% capacity used (Green)
- **Busy**: 75-99% capacity used (Yellow)
- **Overloaded**: ≥ 100% capacity used (Red)

## Best Practices

1. **Start Conservative**: Use default values initially
2. **Calibrate Regularly**: Adjust based on actual data every 2-3 sprints
3. **Team Input**: Get feedback from developers on accuracy
4. **Document Changes**: Track why you adjusted parameters
5. **Consistent Estimation**: Ensure team uses consistent story point scale

## Common Issues

### Capacity Too High
**Symptoms**: Team consistently under-delivers
**Solutions**:
- Decrease focus factor (0.6-0.65)
- Increase hours per story point (5-6)
- Check for hidden work not tracked

### Capacity Too Low
**Symptoms**: Team consistently over-delivers
**Solutions**:
- Increase focus factor (0.75-0.8)
- Decrease hours per story point (3-3.5)
- Verify story point scale is consistent

### Inconsistent Results
**Symptoms**: Varies wildly sprint to sprint
**Solutions**:
- Standardize story point definitions
- Track unplanned work separately
- Consider team stability/changes

## API Access

You can also adjust capacity per user via API:

```bash
curl -X PUT http://localhost:8000/api/capacity/member/{username} \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john.doe",
    "max_story_points": 12
  }'
```

This overrides the calculated capacity for specific users.

## Future Enhancements

Planned improvements:
- [ ] Per-user focus factors
- [ ] Automatic leave hour calculation from OOO records
- [ ] Historical velocity tracking per developer
- [ ] Machine learning-based capacity prediction
- [ ] Holiday calendar integration
- [ ] Part-time developer support

## References

- Scrum Guide: https://scrumguides.org/
- Agile Estimation: https://www.mountaingoatsoftware.com/
- Velocity Tracking: https://www.atlassian.com/agile/project-management/metrics
