"""
aPriori-inspired Design for Manufacturability (DFM) analyzer
Identifies cost drivers and manufacturability issues
"""
from typing import Dict, List, Optional
from PIL import Image

class DFMAnalyzer:
    """
    DFM analyzer inspired by aPriori.
    Identifies features that drive cost or cause manufacturability issues.
    """
    
    def analyze_dfm(self, analysis: Dict, cost_result: Dict) -> Dict:
        """
        Analyze design for manufacturability.
        Identifies cost drivers and potential issues.
        """
        issues = []
        cost_drivers = []
        recommendations = []
        
        dims = analysis.get('dimensions', {})
        features = analysis.get('features', [])
        
        # Check for tight tolerances
        if analysis.get('has_tight_tolerances'):
            issues.append({
                'type': 'tight_tolerance',
                'severity': 'high',
                'message': 'Tight tolerances (< ±0.05mm) detected',
                'cost_impact': '30% surcharge applied',
                'recommendation': 'Consider relaxing tolerances if possible'
            })
            cost_drivers.append({
                'feature': 'Tight Tolerances',
                'cost_impact': cost_result.get('overhead', 0) * 0.3,
                'percentage': 30
            })
        
        # Check for deep features (expensive)
        if dims.get('inner_diameter_mm') and dims.get('max_diameter_mm'):
            wall_thickness = (dims['max_diameter_mm'] - dims.get('inner_diameter_mm', 0)) / 2
            if wall_thickness < 2:
                issues.append({
                    'type': 'thin_wall',
                    'severity': 'medium',
                    'message': f'Thin wall detected: {wall_thickness:.2f}mm',
                    'cost_impact': 'Requires careful machining, higher scrap rate',
                    'recommendation': 'Consider increasing wall thickness if design allows'
                })
        
        # Check for small features
        for feature in features:
            if feature.get('type') == 'hole':
                hole_dia = feature.get('diameter_mm', 0)
                if hole_dia < 1:
                    issues.append({
                        'type': 'small_hole',
                        'severity': 'high',
                        'message': f'Very small hole: {hole_dia}mm',
                        'cost_impact': 'Requires special tooling, slower machining',
                        'recommendation': 'Consider larger hole size if possible'
                    })
        
        # Check for high aspect ratio
        if dims.get('length_mm') and dims.get('max_diameter_mm'):
            aspect_ratio = dims['length_mm'] / dims['max_diameter_mm']
            if aspect_ratio > 10:
                issues.append({
                    'type': 'high_aspect_ratio',
                    'severity': 'medium',
                    'message': f'High aspect ratio: {aspect_ratio:.1f}:1',
                    'cost_impact': 'May require special fixturing, higher setup cost',
                    'recommendation': 'Consider design modifications if possible'
                })
        
        # Identify cost drivers
        breakdown = cost_result.get('breakdown', {})
        
        # Material cost driver
        material_cost = cost_result.get('material_cost', 0)
        total_cost = cost_result.get('cost_per_piece', 0)
        if total_cost > 0:
            material_pct = (material_cost / total_cost) * 100
            if material_pct > 50:
                cost_drivers.append({
                    'feature': 'Material Cost',
                    'cost_impact': material_cost,
                    'percentage': material_pct,
                    'recommendation': 'Consider alternative materials or suppliers'
                })
        
        # Machining time driver
        machining_time = cost_result.get('machining_time_min', 0)
        if machining_time > 60:
            cost_drivers.append({
                'feature': 'Long Machining Time',
                'cost_impact': cost_result.get('machining_cost', 0),
                'percentage': (cost_result.get('machining_cost', 0) / total_cost * 100) if total_cost > 0 else 0,
                'recommendation': 'Optimize machining operations or reduce complexity'
            })
        
        # Generate recommendations
        if issues:
            recommendations.append("Review manufacturability issues above")
        if cost_drivers:
            top_driver = max(cost_drivers, key=lambda x: x.get('percentage', 0))
            recommendations.append(f"Focus on reducing {top_driver['feature']} (largest cost driver)")
        
        return {
            'issues': issues,
            'cost_drivers': cost_drivers,
            'recommendations': recommendations,
            'dfm_score': self._calculate_dfm_score(issues),
            'manufacturability': 'good' if len([i for i in issues if i['severity'] == 'high']) == 0 else 'needs_attention'
        }
    
    def _calculate_dfm_score(self, issues: List[Dict]) -> float:
        """Calculate DFM score (0-100, higher is better)."""
        if not issues:
            return 100.0
        
        high_severity = len([i for i in issues if i['severity'] == 'high'])
        medium_severity = len([i for i in issues if i['severity'] == 'medium'])
        
        score = 100.0
        score -= high_severity * 20
        score -= medium_severity * 10
        
        return max(0.0, score)
