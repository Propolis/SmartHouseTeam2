import React, { useState, useEffect } from 'react';
import { Chart } from 'chart.js/auto';
import './style.css';

const App = () => {
    const [temperature, setTemperature] = useState(0);
    const [humidity, setHumidity] = useState(0);
    const [motion, setMotion] = useState("Нет движения");
    const [smoke, setSmoke] = useState("Не обнаружен");
    const [fanThreshold, setFanThreshold] = useState(30);
    const [autoMode, setAutoMode] = useState(false);
    const [led1State, setLed1State] = useState(false);
    const [led2State, setLed2State] = useState(false);
    const [fanState, setFanState] = useState(false);
    const [notifications, setNotifications] = useState([]);

    useEffect(() => {
        const fetchData = () => {
            fetch('/data')
                .then(response => response.json())
                .then(data => {
                    setTemperature(data.temperature);
                    setHumidity(data.humidity);
                    setMotion(data.motion);
                    setSmoke(data.smoke);
                    setFanThreshold(data.fanThreshold);
                    setAutoMode(data.autoMode);
                    setLed1State(data.led1State);
                    setLed2State(data.led2State);
                    setFanState(data.fanState);

                    if (data.motion === "Обнаружено") {
                        addNotification("Движение обнаружено");
                    }
                    if (data.smoke === "Обнаружен") {
                        addNotification("Дым обнаружен");
                    }
                });
        };

        const interval = setInterval(fetchData, 2000);
        return () => clearInterval(interval);
    }, []);

    const addNotification = (message) => {
        const now = new Date();
        const time = now.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
        const newNotification = { message, time };
        setNotifications(prev => [newNotification, ...prev].slice(0, 10));
    };

    const toggleLED1 = () => {
        fetch('/toggleLED1')
            .then(response => response.text())
            .then(text => setLed1State(text.trim() === 'ВКЛ'));
    };

    const toggleLED2 = () => {
        fetch('/toggleLED2')
            .then(response => response.text())
            .then(text => setLed2State(text.trim() === 'ВКЛ'));
    };

    const toggleFan = () => {
        fetch('/toggleFan')
            .then(response => response.text())
            .then(text => setFanState(text.trim() === 'ВКЛ'));
    };

    const setFanThresholdValue = () => {
        const threshold = document.getElementById('fanThresholdInput').value;
        fetch('/setFanThreshold?threshold=' + threshold)
            .then(response => response.text())
            .then(text => {
                alert(text);
                setFanThreshold(threshold);
            });
    };

    const toggleAutoMode = () => {
        fetch('/toggleAutoMode')
            .then(response => response.text())
            .then(text => {
                alert(text);
                setAutoMode(prev => !prev);
            });
    };

    return (
        <div>
            <Header />
            <Tabs />
            <Microclimate
                temperature={temperature}
                humidity={humidity}
                fanThreshold={fanThreshold}
                autoMode={autoMode}
                fanState={fanState}
                toggleFan={toggleFan}
                setFanThresholdValue={setFanThresholdValue}
                toggleAutoMode={toggleAutoMode}
            />
            <Lighting
                led1State={led1State}
                led2State={led2State}
                toggleLED1={toggleLED1}
                toggleLED2={toggleLED2}
            />
            <Sensors
                motion={motion}
                smoke={smoke}
                notifications={notifications}
            />
        </div>
    );
};

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

const Tabs = () => {
    const [activeTab, setActiveTab] = useState('Microclimate');

    const openTab = (tabName) => {
        setActiveTab(tabName);
    };

    return (
        <div>
            <div className="tab">
                <button className={`tablinks ${activeTab === 'Microclimate' ? 'active' : ''}`} onClick={() => openTab('Microclimate')}>Микроклимат</button>
                <button className={`tablinks ${activeTab === 'Lighting' ? 'active' : ''}`} onClick={() => openTab('Lighting')}>Освещение</button>
                <button className={`tablinks ${activeTab === 'Sensors' ? 'active' : ''}`} onClick={() => openTab('Sensors')}>Датчики</button>
            </div>
            <div className="tabcontent" style={{ display: activeTab === 'Microclimate' ? 'block' : 'none' }}>
                <Microclimate />
            </div>
            <div className="tabcontent" style={{ display: activeTab === 'Lighting' ? 'block' : 'none' }}>
                <Lighting />
            </div>
            <div className="tabcontent" style={{ display: activeTab === 'Sensors' ? 'block' : 'none' }}>
                <Sensors />
            </div>
        </div>
    );
};

const Microclimate = ({ temperature, humidity, fanThreshold, autoMode, fanState, toggleFan, setFanThresholdValue, toggleAutoMode }) => {
    return (
        <div>
            <h2>Микроклимат</h2>
            <p>Температура: {temperature} C</p>
            <p>Влажность: {humidity} %</p>
            <div>
                <div className="chart-container">
                    <canvas id="temperatureChart"></canvas>
                </div>
                <div className="chart-container">
                    <canvas id="humidityChart"></canvas>
                </div>
            </div>
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
                <p>Порог вентилятора: {fanThreshold} C</p>
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

const Lighting = ({ led1State, led2State, toggleLED1, toggleLED2 }) => {
    return (
        <div>
            <h2>Управление освещением</h2>
            <div className="light-tile">
                <img src="https://cdn-icons-png.flaticon.com/512/702/702814.png" alt="Лампочка" />
                <h3>Гостиная</h3>
                <p>Свет</p>
                <label className="switch">
                    <input type="checkbox" checked={led1State} onChange={toggleLED1} />
                    <span className="slider"></span>
                </label>
            </div>
            <div className="light-tile">
                <img src="https://cdn-icons-png.flaticon.com/512/702/702814.png" alt="Лампочка" />
                <h3>Спальня</h3>
                <p>Свет</p>
                <label className="switch">
                    <input type="checkbox" checked={led2State} onChange={toggleLED2} />
                    <span className="slider"></span>
                </label>
            </div>
        </div>
    );
};

const Sensors = ({ motion, smoke, notifications }) => {
    return (
        <div>
            <h2>Датчики</h2>
            <p>Движение: {motion}</p>
            <p>Дым: {smoke}</p>
            <div className="notifications">
                <h3>Уведомления</h3>
                <div id="notifications">
                    {notifications.map((notification, index) => (
                        <div key={index} className="notification">
                            <strong>{notification.time}</strong>: {notification.message}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default App;