def get_explanation(db, language: str = 'en') -> dict:
    """Generate a structured explanation of current risk situation."""
    from app.services.prediction_service import get_predictions
    
    pred_data = get_predictions(db)
    predictions = pred_data['predictions']
    
    # Sort by risk probability, highest first
    sorted_preds = sorted(predictions, key=lambda p: p['risk_probability'], reverse=True)
    high_risk = [p for p in sorted_preds if p['risk_level'] == 'high']
    
    if language == 'mr':
        # Marathi templates
        if high_risk:
            highest = high_risk[0]
            summary = f"सध्या {highest['zone_id']} झोनमध्ये सर्वाधिक अंदाजित धोका ({highest['risk_probability']:.0%}) आहे."
            reasoning = "गर्दीची घनता वाढत आहे आणि पाण्याची उपलब्धता कमी होत आहे."
        else:
            summary = "सध्या कोणत्याही झोनमध्ये उच्च धोका नाही."
            reasoning = "सर्व झोनमध्ये सामान्य परिस्थिती आहे."
        confidence_caveat = f"धोक्याची शक्यता {pred_data['model_version']} मॉडेलमधून आली आहे."
    else:
        # English templates
        if high_risk:
            highest = high_risk[0]
            zone_names = ', '.join([p['zone_id'] for p in high_risk])
            summary = f"{highest['zone_id']} has the highest predicted risk at {highest['risk_probability']:.0%}. High-risk zones: {zone_names}."
            reasoning = "Crowd density is increasing while water availability is decreasing in these zones. High temperature and humidity amplify the risk."
        else:
            summary = "No zones are currently at high risk."
            reasoning = "All zones show normal operating conditions."
        confidence_caveat = f"Risk probability comes from the {pred_data['model_version']} model. Predictions are generated every decision cycle and may change as conditions evolve."
    
    return {
        'language': language,
        'summary': summary,
        'reasoning': reasoning,
        'confidence_caveat': confidence_caveat,
    }
