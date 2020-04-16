const minMax = {
  min: 'min-content',
  max: 'max-content',
}
module.exports = {
  theme: {
    extend: {
      width: minMax,
      height: minMax,
      colors: {
        'text': 'var(--text-color)',
        'neutral': {
          "10": "var(--neutral-10)",
          "20": "var(--neutral-20)",
          "30": "var(--neutral-30)",
          "40": "var(--neutral-40)",
          "50": "var(--neutral-50)",
          "60": "var(--neutral-60)",
          "70": "var(--neutral-70)",
          "80": "var(--neutral-80)",
          "90": "var(--neutral-90)"
        },
        'primary': {
          "10": "var(--primary-10)",
          "20": "var(--primary-20)",
          "30": "var(--primary-30)",
          "40": "var(--primary-40)",
          "50": "var(--primary-50)",
          "60": "var(--primary-60)",
          "70": "var(--primary-70)",
          "80": "var(--primary-80)",
          "90": "var(--primary-90)"
        },
        'secondary': {
          "10": "var(--secondary-10)",
          "20": "var(--secondary-20)",
          "30": "var(--secondary-30)",
          "40": "var(--secondary-40)",
          "50": "var(--secondary-50)",
          "60": "var(--secondary-60)",
          "70": "var(--secondary-70)",
          "80": "var(--secondary-80)",
          "90": "var(--secondary-90)"
        }
      }
    }
  },
  variants: {
    boxShadow: ['responsive', 'group-hover', 'focus-within', 'hover', 'focus', 'active']
  },
  plugins: []
}
