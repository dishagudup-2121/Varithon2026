import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Check } from 'lucide-react';
import logoImg from '../assets/logo_varithon.png';

function Signup() {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    confirmPassword: '',
    language: 'en'
  });
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    if (errors[e.target.name]) {
      setErrors({
        ...errors,
        [e.target.name]: ''
      });
    }
  };

  const handleLanguageSelect = (language) => {
    setFormData({
      ...formData,
      language
    });
    if (errors.language) {
      setErrors({
        ...errors,
        language: ''
      });
    }
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.fullName.trim()) {
      newErrors.fullName = t('validation.nameRequired');
    }

    if (!formData.email.trim()) {
      newErrors.email = t('validation.emailRequired');
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = t('validation.emailInvalid');
    }

    if (!formData.password) {
      newErrors.password = t('validation.passwordRequired');
    } else if (formData.password.length < 6) {
      newErrors.password = t('validation.passwordShort');
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = t('validation.passwordMismatch');
    }

    if (!formData.language) {
      newErrors.language = t('validation.languageRequired');
    }

    return newErrors;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const newErrors = validate();

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    const userData = {
      name: formData.fullName,
      email: formData.email,
      language: formData.language
    };

    localStorage.setItem('varisetuUser', JSON.stringify(userData));
    i18n.changeLanguage(formData.language);
    localStorage.setItem('varisetuLanguage', formData.language);

    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-[#FFFDF8] flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-lg">
        {/* Logo at top */}
        <Link to="/" className="flex flex-col items-center justify-center mb-5">
          <img 
            src={logoImg} 
            alt="VariSetu Logo" 
            width="80"
            height="80"
            className="h-[80px] w-[80px] object-contain mb-1.5"
          />
          <span className="text-2xl font-extrabold text-[#E86F00] tracking-tight">VariSetu</span>
          <p className="text-xs text-[#806B59] mt-0.5">Technology that walks with the Wari.</p>
        </Link>

        {/* Card */}
        <div className="bg-white rounded-3xl shadow-xl p-6 sm:p-8 border border-[#F1DEC8]">
          <h1 className="text-2xl font-bold text-[#392719] mb-1.5">
            {t('auth.joinVarisetu')}
          </h1>
          <p className="text-sm text-[#806B59] mb-5">
            {t('auth.chooseExperience')}
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Full Name */}
            <div>
              <label htmlFor="fullName" className="block text-xs font-semibold uppercase tracking-wider text-[#6B421F] mb-1.5">
                {t('auth.fullName')}
              </label>
              <input
                type="text"
                id="fullName"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                className={`w-full px-4 py-2.5 border ${errors.fullName ? 'border-red-500' : 'border-[#EDE2D0]'} rounded-xl bg-[#FFFDF8] text-sm text-[#3D2918] focus:outline-none focus:border-[#F28C00] focus:ring-1 focus:ring-[#F28C00]`}
                placeholder="Your full name"
              />
              {errors.fullName && <p className="mt-1 text-xs text-red-500">{errors.fullName}</p>}
            </div>

            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-xs font-semibold uppercase tracking-wider text-[#6B421F] mb-1.5">
                {t('auth.email')}
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={`w-full px-4 py-2.5 border ${errors.email ? 'border-red-500' : 'border-[#EDE2D0]'} rounded-xl bg-[#FFFDF8] text-sm text-[#3D2918] focus:outline-none focus:border-[#F28C00] focus:ring-1 focus:ring-[#F28C00]`}
                placeholder="your@email.com"
              />
              {errors.email && <p className="mt-1 text-xs text-red-500">{errors.email}</p>}
            </div>

            {/* Password */}
            <div>
              <label htmlFor="password" className="block text-xs font-semibold uppercase tracking-wider text-[#6B421F] mb-1.5">
                {t('auth.password')}
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className={`w-full px-4 py-2.5 border ${errors.password ? 'border-red-500' : 'border-[#EDE2D0]'} rounded-xl bg-[#FFFDF8] text-sm text-[#3D2918] focus:outline-none focus:border-[#F28C00] focus:ring-1 focus:ring-[#F28C00]`}
                placeholder="••••••••"
              />
              {errors.password && <p className="mt-1 text-xs text-red-500">{errors.password}</p>}
            </div>

            {/* Confirm Password */}
            <div>
              <label htmlFor="confirmPassword" className="block text-xs font-semibold uppercase tracking-wider text-[#6B421F] mb-1.5">
                {t('auth.confirmPassword')}
              </label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className={`w-full px-4 py-2.5 border ${errors.confirmPassword ? 'border-red-500' : 'border-[#EDE2D0]'} rounded-xl bg-[#FFFDF8] text-sm text-[#3D2918] focus:outline-none focus:border-[#F28C00] focus:ring-1 focus:ring-[#F28C00]`}
                placeholder="••••••••"
              />
              {errors.confirmPassword && <p className="mt-1 text-xs text-red-500">{errors.confirmPassword}</p>}
            </div>

            {/* Language Selection */}
            <div className="pt-2">
              <label className="block text-xs font-semibold uppercase tracking-wider text-[#6B421F] mb-2">
                {t('auth.chooseLanguage')}
              </label>
              <div className="grid grid-cols-2 gap-3">
                {/* English Card */}
                <button
                  type="button"
                  onClick={() => handleLanguageSelect('en')}
                  className={`relative p-3.5 rounded-xl border-2 transition-all cursor-pointer ${
                    formData.language === 'en'
                      ? 'border-[#F28C00] bg-[#FFF8EC]'
                      : 'border-[#EDE2D0] hover:border-[#F28C00]/50'
                  }`}
                >
                  {formData.language === 'en' && (
                    <div className="absolute top-2 right-2">
                      <Check className="w-4 h-4 text-[#E86F00]" strokeWidth={3} />
                    </div>
                  )}
                  <div className="text-center">
                    <p className="text-base font-bold text-[#3D2918]">English</p>
                    <p className="text-xs text-[#806B59]">Continue in English</p>
                  </div>
                </button>

                {/* Marathi Card */}
                <button
                  type="button"
                  onClick={() => handleLanguageSelect('mr')}
                  className={`relative p-3.5 rounded-xl border-2 transition-all cursor-pointer ${
                    formData.language === 'mr'
                      ? 'border-[#F28C00] bg-[#FFF8EC]'
                      : 'border-[#EDE2D0] hover:border-[#F28C00]/50'
                  }`}
                >
                  {formData.language === 'mr' && (
                    <div className="absolute top-2 right-2">
                      <Check className="w-4 h-4 text-[#E86F00]" strokeWidth={3} />
                    </div>
                  )}
                  <div className="text-center">
                    <p className="text-base font-bold text-[#3D2918]">मराठी</p>
                    <p className="text-xs text-[#806B59]">मराठीत पुढे जा</p>
                  </div>
                </button>
              </div>
              {errors.language && <p className="mt-1 text-xs text-red-500">{errors.language}</p>}
            </div>

            {/* Create Account Button */}
            <button
              type="submit"
              className="w-full mt-4 py-3.5 bg-gradient-to-r from-[#F28C00] to-[#FF5A00] text-white rounded-xl hover:from-[#E86F00] hover:to-[#E05000] transition font-bold text-base shadow-md hover:shadow-lg cursor-pointer"
            >
              {t('auth.createAccountBtn')}
            </button>
          </form>

          {/* Login Link */}
          <div className="mt-5 text-center text-sm border-t border-[#F1DEC8] pt-4">
            <p className="text-[#806B59]">
              {t('auth.haveAccount')}{' '}
              <Link to="/login" className="text-[#E86F00] hover:text-[#D96F00] font-bold">
                {t('auth.signIn')}
              </Link>
            </p>
          </div>
        </div>

        {/* Back to Home */}
        <div className="mt-5 text-center">
          <Link to="/" className="text-xs text-[#806B59] hover:text-[#E86F00] transition">
            ← Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Signup;
