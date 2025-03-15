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
        fetch('/data')
            .then(response => response.json())
            .then(result => {
                console.log('Результат запроса:', result);
                const data = result.data || result;
                console.log('Извлеченные данные:', data);
                setTemperature(data.temperature);
                setHumidity(data.humidity);
                setMotion(data.motion);
                setSmoke(data.smoke);
                setFanThreshold(data.fanThreshold);
                setAutoMode(data.autoMode);
                setLed1State(data.State_of_Lamp_Bedroom);
                setLed2State(data.State_of_Lamp_Bathroom);
                setFanState(data.State_of_Ventilation);

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

    // const toggleLED1 = () => {
    //     fetch('/toggleLED1')
    //         .then(response => response.text())
    //         .then(text => setLed1State(text.trim() === 'ВКЛ'));
    // };
    //
    // const toggleLED2 = () => {
    //     fetch('/toggleLED2')
    //         .then(response => response.text())
    //         .then(text => setLed2State(text.trim() === 'ВКЛ'));
    // };
    //
    // const toggleFan = () => {
    //     fetch('/toggleFan')
    //         .then(response => response.text())
    //         .then(text => setFanState(text.trim() === 'ВКЛ'));
    // };
        const toggleModule = (moduleName) => {
          fetch(`/api/toggle-module/${moduleName}`, { method: 'POST' })
            .then((response) => response.json())
            .then((data) => {
              const newValue = data[moduleName]; // "0" или "1"
              // Обновляем state для нужного модуля
              if (moduleName === 'Lamp_Bedroom') {
                setLed1State(newValue === "1");
              } else if (moduleName === 'Lamp_Bathroom') {
                setLed2State(newValue === "1");
              }
            })
            .catch((err) => console.error("Ошибка переключения:", err));
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
