import React, { useState, useEffect } from 'react';

function Header() {
    const [currentDateTime, setCurrentDateTime] = useState({
        date: 'Загрузка...',
        time: 'Загрузка...',
    });

    // Функция для обновления даты и времени
    const updateDateTime = () => {
        const now = new Date();
        const date = now.toLocaleDateString('ru-RU');
        const time = now.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
        setCurrentDateTime({ date, time });
    };

    // Обновляем время каждую секунду
    useEffect(() => {
        updateDateTime(); // Первоначальное обновление
        const interval = setInterval(updateDateTime, 1000); // Обновление каждую секунду
        return () => clearInterval(interval); // Очистка интервала при размонтировании компонента
    }, []);

    return (
        <div className="header">
            <h1>
                <img src="https://cdn-icons-png.flaticon.com/512/619/619032.png" alt="Эмблема" />
                "Прекрасное название"
            </h1>
            <div className="info" id="dateTime">
                <div>Ростов-на-Дону</div>
                <div>{currentDateTime.date}</div>
                <div>{currentDateTime.time}</div>
            </div>
        </div>
    );
}

export default Header;