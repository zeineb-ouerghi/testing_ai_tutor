import React from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut, User } from 'lucide-react';

const Layout = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="min-h-screen flex flex-col bg-background">
            <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-blue-100 px-6 py-4 flex justify-between items-center shadow-sm">
                <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate('/')}>
                    <div className="w-8 h-8 bg-gradient-to-tr from-primary-600 to-primary-400 rounded-lg flex items-center justify-center text-white font-bold text-xl shadow-lg shadow-primary-500/30">
                        P
                    </div>
                    <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-700 to-primary-500">Praxis</h1>
                </div>
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2 text-slate-600 bg-white/50 px-3 py-1.5 rounded-full border border-blue-100">
                        <User size={18} className="text-primary-500" />
                        <span className="font-medium text-sm">{user?.name}</span>
                    </div>
                    <button
                        onClick={handleLogout}
                        className="p-2 hover:bg-red-50 hover:text-red-500 rounded-full text-slate-400 transition-all duration-200"
                        title="Logout"
                    >
                        <LogOut size={20} />
                    </button>
                </div>
            </header>
            <main className="flex-1 overflow-hidden">
                <Outlet />
            </main>
        </div>
    );
};

export default Layout;
