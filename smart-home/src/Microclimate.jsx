// Microclimate.jsx
import React from 'react';

const Microclimate = ({ temperature, humidity, fanThreshold, autoMode, fanState, toggleFan, setFanThresholdValue, toggleAutoMode }) => {
    return (
        <div>
            <h2>Микроклимат</h2>
            <p>Температура: {temperature}°C</p>
            <p>Влажность: {humidity}%</p>
            <h2>Управление вентилятором</h2>
            <div className="fan-tile">
                <img src="https://cdn-icons-png.flaticon.com/512/979/979619.png" alt="Вентилятор" />
                <h3>Вентилятор</h3>
                <label className="switch">
                    <input type="checkbox" checked={fanState} onChange={toggleFan} />
                    <span className="slider"></span>
                </label>
            </div>
            <div className="flex-row">
                <p>Порог вентилятора: {fanThreshold}°C</p>
                <input type="number" id="fanThresholdInput" placeholder="Введите порог" />
                <button onClick={setFanThresholdValue}>Установить</button>
            </div>
            <div className="flex-row">
                <p>Режим управления: {autoMode ? 'Автоматический' : 'Ручной'}</p>
                <button onClick={toggleAutoMode}>Переключить режим</button>
            </div>
        </div>
    );
};

export default Microclimate;
