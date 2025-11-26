import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Brain } from 'lucide-react';

const Login = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [agreed, setAgreed] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!agreed) return;

        const success = await login(name, email);
        if (success) {
            navigate('/');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-50">
            <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-slate-100">
                <div className="flex flex-col items-center mb-8">
                    <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-4 text-primary">
                        <Brain size={32} />
                    </div>
                    <h1 className="text-3xl font-bold text-slate-800">Welcome to Praxis</h1>
                    <p className="text-slate-500 mt-2">Your AI Tutor Platform</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">Full Name</label>
                        <input
                            type="text"
                            required
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all"
                            placeholder="Jane Doe"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">Email Address</label>
                        <input
                            type="email"
                            required
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all"
                            placeholder="jane@example.com"
                        />
                    </div>

                    <div className="flex items-start gap-3 p-4 bg-slate-50 rounded-lg border border-slate-200">
                        <input
                            type="checkbox"
                            id="terms"
                            required
                            checked={agreed}
                            onChange={(e) => setAgreed(e.target.checked)}
                            className="mt-1 w-4 h-4 text-primary rounded focus:ring-primary"
                        />
                        <label htmlFor="terms" className="text-sm text-slate-600 leading-relaxed">
                            I understand that this is an AI-powered educational tool. Information provided may not always be accurate. I agree to the Terms of Service.
                        </label>
                    </div>

                    <button
                        type="submit"
                        disabled={!agreed}
                        className="w-full bg-primary text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-lg shadow-primary/20"
                    >
                        Start Learning
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Login;
