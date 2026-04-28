---
name: Clinical Precision System
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#424750'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#727781'
  outline-variant: '#c2c6d2'
  surface-tint: '#2260a1'
  primary: '#003c6f'
  on-primary: '#ffffff'
  primary-container: '#0b5394'
  on-primary-container: '#a2c8ff'
  inverse-primary: '#a4c9ff'
  secondary: '#48626e'
  on-secondary: '#ffffff'
  secondary-container: '#cbe7f5'
  on-secondary-container: '#4e6874'
  tertiary: '#602d00'
  on-tertiary: '#ffffff'
  tertiary-container: '#833f00'
  on-tertiary-container: '#ffb584'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d4e3ff'
  primary-fixed-dim: '#a4c9ff'
  on-primary-fixed: '#001c39'
  on-primary-fixed-variant: '#004883'
  secondary-fixed: '#cbe7f5'
  secondary-fixed-dim: '#afcbd8'
  on-secondary-fixed: '#021f29'
  on-secondary-fixed-variant: '#304a55'
  tertiary-fixed: '#ffdcc7'
  tertiary-fixed-dim: '#ffb787'
  on-tertiary-fixed: '#311300'
  on-tertiary-fixed-variant: '#723600'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  h1-report-title:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.02em
  h2-section-header:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  data-mono:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-caps:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  container-margin: 24px
  gutter: 16px
  stack-compact: 8px
  stack-comfortable: 16px
  section-gap: 32px
---

## Brand & Style

The design system is engineered for high-stakes medical environments where clarity and rapid interpretation are paramount. It prioritizes a **Corporate Modern** aesthetic, moving away from consumer-grade "softness" in favor of a rigorous, institutional feel that evokes authority and reliability.

The target audience consists of cardiologists, technicians, and clinical staff who require a tool that minimizes cognitive load during EKG analysis. The style utilizes a structured, grid-based approach with an emphasis on data density, ensuring that complex wave patterns and patient metrics are the focal point without visual distraction. The emotional response is one of calm competence and scientific rigor.

## Colors

The palette is anchored by **Medical Blue (#0B5394)**, a deep, trustworthy primary hue that provides excellent contrast against white backgrounds. The neutral scale relies on "Professional Grises"—cool-toned slates that prevent visual fatigue and create a sophisticated, sterile environment.

Clinical urgency is communicated through a strictly enforced semantic scale:
- **Critical (Red):** Reserved exclusively for life-threatening arrhythmias or immediate action items.
- **Caution (Yellow):** Used for borderline readings or technical artifacts requiring review.
- **Normal (Green):** Indicates baseline health or successfully processed data.

Backgrounds utilize clean whites and very light grays to separate report sections, maintaining a high-contrast environment suitable for diverse lighting conditions in clinical settings.

## Typography

The design system utilizes **Inter** for its exceptional legibility at small sizes and its neutral, systematic character. The hierarchy is designed for "skimmability" in medical reports, where practitioners must quickly locate patient identifiers and diagnostic conclusions.

- **Data Presentation:** Numerical values (BPM, PR interval, QRS duration) use slightly tighter tracking and medium weights to stand out from descriptive text.
- **Hierarchy:** High contrast in weight (Bold vs. Regular) is preferred over excessive variation in font size to maintain high data density.
- **Labels:** Small caps are used for metadata labels (e.g., "DATE OF BIRTH", "LEAD II") to distinguish them from dynamic patient data.

## Layout & Spacing

This design system employs a **Fixed Grid** model for report views to ensure EKG waveforms maintain consistent aspect ratios across various screen sizes, which is critical for visual diagnosis. 

The spacing rhythm is based on a **4px base unit**. To support high data density, internal padding within cards and tables is kept compact (8px-12px), while larger gaps (32px) are used to separate distinct diagnostic sections. This "proximity-based grouping" allows the user to perceive the report structure without the need for heavy visual dividers.

## Elevation & Depth

To maintain a professional and "high-trust" appearance, the design system avoids heavy shadows or trendy blurs. Instead, it utilizes **Tonal Layers** and **Low-contrast Outlines**.

- **Surfaces:** The primary workspace is #FFFFFF. Secondary information panels use #F5F5F5.
- **Borders:** Elements are defined by subtle 1px borders in #E0E0E0. This creates a "blueprint" feel that emphasizes structure.
- **Interaction Depth:** Only the most critical interactive elements (like a "Confirm Diagnosis" button) receive a subtle, low-opacity ambient shadow to indicate clickability. Everything else remains flat to keep the focus on the data.

## Shapes

The design system uses a **Soft (0.25rem)** roundedness level. This subtle rounding provides a modern feel without appearing "bubbly" or informal. It strikes a balance between the clinical coldness of sharp corners and the overly friendly nature of consumer apps. 

Containers for EKG strips should maintain sharp 90-degree corners or a maximum of 2px radius to avoid clipping the grid lines essential for manual measurements.

## Components

- **Buttons:** Primary buttons use the Medical Blue background with white text. They are rectangular with a 4px radius. No gradients. Secondary buttons use a gray border with a clear background.
- **Status Chips:** Small, high-contrast badges for "Critical," "Normal," and "Artifact." Use a subtle background tint of the semantic color with a high-contrast dark text or a bold 2px left-border.
- **Data Tables:** Use "Professional Grise" (#F8F9FA) for header rows. No vertical borders; use subtle horizontal dividers only.
- **EKG Waveform Container:** A specialized component with a strictly white background and a faint red or light gray grid overlay. 
- **Input Fields:** Minimalist design with a 1px #E0E0E0 border that thickens and changes to Medical Blue on focus.
- **Metric Cards:** Compact containers for vitals, featuring a large numerical value and a "Label-Caps" subtitle for the metric name.
- **Clinical Alerts:** Topped with a heavy color bar corresponding to the semantic scale (Red/Yellow) to ensure they are the first thing a user sees upon opening a report.