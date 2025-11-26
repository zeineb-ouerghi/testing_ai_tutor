import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { BookOpen, Code, MessageSquare, Terminal, GraduationCap } from 'lucide-react';

const icons = {
    assessment: GraduationCap,
    fundamentals: BookOpen,
    advanced: Terminal,
    practice: Code,
    genai_fundamentals: MessageSquare,
};

const Dashboard = () => {
    const [modules, setModules] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchModules = async () => {
            try {
                const res = await axios.get('http://localhost:8000/modules/');
                setModules(res.data);
            } catch (err) {
                console.error("Failed to fetch modules", err);
            }
        };
        fetchModules();
    }, []);

    return (
        <div className="p-8 max-w-7xl mx-auto">
            <h2 className="text-3xl font-bold text-slate-800 mb-2">Learning Experiences</h2>
            <p className="text-slate-500 mb-8">Select a module to begin your journey.</p>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {modules.map((module) => {
                    const Icon = icons[module.id] || BookOpen;
                    return (
                        <div
                            key={module.id}
                            onClick={() => navigate(`/chat/${module.id}`)}
                            className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm hover:shadow-md hover:border-primary/50 cursor-pointer transition-all group"
                        >
                            <div className="w-12 h-12 bg-blue-50 text-primary rounded-lg flex items-center justify-center mb-4 group-hover:bg-primary group-hover:text-white transition-colors">
                                <Icon size={24} />
                            </div>
                            <h3 className="text-xl font-bold text-slate-800 mb-2">{module.title}</h3>
                            <p className="text-slate-600 leading-relaxed">{module.description}</p>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default Dashboard;
