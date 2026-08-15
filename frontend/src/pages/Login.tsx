import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import logoImg from '../assets/logo_varithon.png';

interface LoginFormData {
  email: string;
  password: string;
}

interface LoginErrors {
  email?: string;
  password?: string;
}

function Login() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [formData, setFormData] = useState<LoginFormData>({
    email: '',
    password: ''
  });
  const [errors, setErrors] = useState<LoginErrors>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    if (errors[name as keyof LoginErrors]) {
      setErrors({
        ...errors,
        [name]: ''
      });
    }
  };

  const validate = () => {
    const newErrors: LoginErrors = {};

    if (!formData.email.trim()) {
      newErrors.email = t('validation.emailRequired');
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = t('validation.emailInvalid');
    }

    if (!formData.password) {
      newErrors.password = t('validation.passwordRequired');
    }

    return newErrors;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: LoginErrors = validate();

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    const userData = {
      name: formData.email.split('@')[0],
      email: formData.email,
      language: localStorage.getItem('varisetuLanguage') || 'en'
    };

    localStorage.setItem('varisetuUser', JSON.stringify(userData));
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-[#FFFDF8] flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-md">
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
        <div className="bg-white rounded-3xl shadow-xl p-8 border border-[#F1DEC8]">
          <h1 className="text-2xl font-bold text-[#392719] mb-1.5">
            {t('auth.welcomeBack')}
          </h1>
          <p className="text-sm text-[#806B59] mb-6">
            {t('auth.continueJourney')}
          </p>

          <form onSubmit={handleSubmit} className="space-y-5">
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
                className={`w-full px-4 py-3 border ${errors.email ? 'border-red-500' : 'border-[#EDE2D0]'} rounded-xl bg-[#FFFDF8] text-sm text-[#3D2918] focus:outline-none focus:border-[#F28C00] focus:ring-1 focus:ring-[#F28C00]`}
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
                className={`w-full px-4 py-3 border ${errors.password ? 'border-red-500' : 'border-[#EDE2D0]'} rounded-xl bg-[#FFFDF8] text-sm text-[#3D2918] focus:outline-none focus:border-[#F28C00] focus:ring-1 focus:ring-[#F28C00]`}
                placeholder="••••••••"
              />
              {errors.password && <p className="mt-1 text-xs text-red-500">{errors.password}</p>}
            </div>

            {/* Forgot Password */}
            <div className="text-right">
              <button type="button" className="text-xs font-medium text-[#E86F00] hover:text-[#D96F00] cursor-pointer">
                {t('auth.forgotPassword')}
              </button>
            </div>

            {/* Login Button */}
            <button
              type="submit"
              className="w-full py-3.5 bg-gradient-to-r from-[#F28C00] to-[#FF5A00] text-white rounded-xl hover:from-[#E86F00] hover:to-[#E05000] transition font-bold text-base shadow-md hover:shadow-lg cursor-pointer"
            >
              {t('auth.login')}
            </button>
          </form>

          {/* Sign Up Link */}
          <div className="mt-6 text-center text-sm border-t border-[#F1DEC8] pt-5">
            <p className="text-[#806B59]">
              {t('auth.noAccount')}{' '}
              <Link to="/signup" className="text-[#E86F00] hover:text-[#D96F00] font-bold">
                {t('auth.createAccount')}
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

export default Login;
