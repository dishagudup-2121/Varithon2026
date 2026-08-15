import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import enTranslation from './locales/en/translation.json';
import mrTranslation from './locales/mr/translation.json';

// Get saved language from localStorage or default to 'en'
const savedLanguage = localStorage.getItem('varisetuLanguage') || 'en';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        translation: enTranslation
      },
      mr: {
        translation: mrTranslation
      }
    },
    lng: savedLanguage,
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

// Save language preference whenever it changes
i18n.on('languageChanged', (lng) => {
  localStorage.setItem('varisetuLanguage', lng);
});

export default i18n;
