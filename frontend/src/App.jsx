import React, { useState, useEffect } from 'react';
import Header from './Header';
import Tabs from './Tabs';
import Microclimate from './Microclimate';
import Lighting from './Lighting';
import Sensors from './Sensors';
import './style.css';

const App = () => {
    // Состояния для данных
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
    const [activeTab, setActiveTab] = useState('Microclimate');

    // Функция для получения данных с сервера
    const fetchData = () => {
        fetch('/data') // GET-запрос для получения данных
            .then(response => response.json())
            .then(data => {
		console.log("Результат запроса:", data);
                setTemperature(data.temperature);
                setHumidity(data.humidity);
                setMotion(data.motion);
                setSmoke(data.smoke);
                setFanThreshold(data.fanThreshold);
                setAutoMode(data.autoMode);
                setLed1State(data.State_of_Lamp_Bedroom);
                setLed2State(data.State_of_Lamp_Bathroom);
                setFanState(data.State_of_Ventilation);

                // Добавление уведомлений
                if (data.motion === "Обнаружено") {
                    addNotification("Движение обнаружено");
                }
                if (data.smoke === "Обнаружен") {
                    addNotification("Дым обнаружен");
                }
            })
            .catch(err => console.error("Ошибка получения данных:", err));
    };

    // Запуск периодического обновления данных
    useEffect(() => {
        fetchData(); // Первоначальный запрос данных
        const interval = setInterval(fetchData, 2000); // Обновление каждые 2 секунды
        return () => clearInterval(interval); // Очистка интервала при размонтировании
    }, []);

    // Функция для добавления уведомлений
    const addNotification = (message) => {
        const now = new Date();
        const time = now.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
        const newNotification = { message, time };
        setNotifications(prev => [newNotification, ...prev].slice(0, 10)); // Ограничение до 10 уведомлений
    };

    // Функции для управления устройствами
    const toggleLED1 = () => {
        fetch('/api/toggle-module/Lamp_Bedroom', { method: 'POST' }) // Указываем метод POST
            .then(response => response.text())
            .then(text => setLed1State(text.trim() === 'ВКЛ'))
            .catch(err => console.error("Ошибка переключения LED1:", err));
    };

    const toggleLED2 = () => {
        fetch('/api/toggle-module/Lamp_Bathroom', { method: 'POST' }) // Указываем метод POST
            .then(response => response.text())
            .then(text => setLed2State(text.trim() === 'ВКЛ'))
            .catch(err => console.error("Ошибка переключения LED2:", err));
    };

    const toggleFan = () => {
        fetch('/api/toggle-module/Ventilation', { method: 'POST' }) // Указываем метод POST
            .then(response => response.text())
            .then(text => setFanState(text.trim() === 'ВКЛ'))
            .catch(err => console.error("Ошибка переключения вентилятора:", err));
    };

    const setFanThresholdValue = () => {
        const threshold = document.getElementById('fanThresholdInput').value;
        fetch('/api/toggle-module/fanThreshold', {
            method: 'POST', // Указываем метод POST
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ threshold }), // Передаем порог в теле запроса
        })
            .then(response => response.text())
            .then(text => {
                alert(text);
                setFanThreshold(threshold);
            })
            .catch(err => console.error("Ошибка установки порога вентилятора:", err));
    };

    const toggleAutoMode = () => {
        fetch('/api/toggle-module/autoMode', { method: 'POST' }) // Указываем метод POST
            .then(response => response.text())
            .then(text => {
                alert(text);
                setAutoMode(prev => !prev);
            })
            .catch(err => console.error("Ошибка переключения режима:", err));
    };

    return (
        <div>
            <Header />
            <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />
            {activeTab === 'Microclimate' && (
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
            )}
            {activeTab === 'Lighting' && (
                <Lighting
                    led1State={led1State}
                    led2State={led2State}
                    toggleLED1={toggleLED1}
                    toggleLED2={toggleLED2}
                />
            )}
            {activeTab === 'Sensors' && (
                <Sensors
                    motion={motion}
                    smoke={smoke}
                    notifications={notifications}
                />
            )}
        </div>
    );
};

export default App;