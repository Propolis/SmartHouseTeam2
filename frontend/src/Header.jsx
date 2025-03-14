// Header.jsx
import React, { useState, useEffect } from 'react';

const Header = () => {
    const [dateTime, setDateTime] = useState({
        date: 'Загрузка...',
        time: 'Загрузка...'
    });

    useEffect(() => {
        const updateDateTime = () => {
            const now = new Date();
            const date = now.toLocaleDateString('ru-RU');
            const time = now.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
            setDateTime({ date, time });
        };

        const interval = setInterval(updateDateTime, 1000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="header">
            <h1>Умный дом</h1>
            <div className="info">
                <div>Ростов-на-Дону</div>
                <div>{dateTime.date}</div>
                <div>{dateTime.time}</div>
            </div>
        </div>
    );
};

export default Header;
