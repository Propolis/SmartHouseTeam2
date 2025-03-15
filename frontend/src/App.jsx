// App.jsx
import React, { useState, useEffect } from 'react';
import Header from './Header';
import Tabs from './Tabs';

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
            // Если не настроен proxy, используйте полный URL:
            fetch('/data')
                .then(response => response.json())
                .then(result => {
                    const data = result.data || result; // Извлекаем данные, если они обёрнуты в "data"
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
                })
                .catch(err => console.error("Ошибка получения данных:", err));
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
            <Tabs
                motion={motion}
                smoke={smoke}
                notifications={notifications}
                temperature={temperature}
                humidity={humidity}
                fanThreshold={fanThreshold}
                autoMode={autoMode}
                fanState={fanState}
                toggleFan={toggleFan}
                setFanThresholdValue={setFanThresholdValue}
                toggleAutoMode={toggleAutoMode}
                led1State={led1State}
                led2State={led2State}
                toggleLED1={toggleLED1}
                toggleLED2={toggleLED2}
            />
        </div>
    );
};

export default App;
