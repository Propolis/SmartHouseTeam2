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
    const [bathHumidity, setBathHumidity] = useState(0);
    const [motion, setMotion] = useState("Нет движения");
    const [smoke, setSmoke] = useState("Не обнаружен");
    const [protechka, setProtechka] = useState("Не обнаружена");
    const [fanThreshold, setFanThreshold] = useState(30);
    const [bathFanThreshold, setBathFanThreshold] = useState(40);
    const [autoMode, setAutoMode] = useState(false);
    const [klimatFanState, setKlimatFanState] = useState(false);
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
            setBathHumidity(data.Humidity_bathroom);
            setMotion(data.motion);
            setSmoke(data.smoke);
            setFanThreshold(data.fanThreshold);
            setBathFanThreshold(data.VlaznostPorog);
            setAutoMode(data.autoMode);

            // Обновление состояния устройств с учетом данных с сервера
            if (data.State_of_Lamp_Bedroom !== led2State) {
                setLed2State(data.State_of_Lamp_Bedroom === "true"); // Обновляем состояние на фронте
            }
            if (data.State_of_Ventilation !== fanState) {
                setFanState(data.State_of_Ventilation === "true"); // Обновляем состояние вентилятора на фронте
            }
            if (data.State_of_Klimat_Kontrol !== klimatFanState) {
                setKlimatFanState(data.State_of_Klimat_Kontrol === "true"); // Обновляем состояние вентилятора на фронте
            }

            // Добавление уведомлений
            if (data.motion === "1") {
                addNotification("Движение обнаружено");
            }
            if (data.smoke === "1") {
                addNotification("Дым обнаружен");
            }
	    if (data.Protechka === "1") {
		setProtechka("Протечка обнаружена");
                addNotification("Протечка обнаружена");
            }
        })
        .catch(err => console.error("Ошибка получения данных:", err));
};


    // Запуск периодического обновления данных
    useEffect(() => {
        fetchData(); // Первоначальный запрос данных
        const interval = setInterval(fetchData, 1000); // Обновление каждые 0.5 секунды
        return () => clearInterval(interval); // Очистка интервала при размонтировании
    }, []);

    // Функция для добавления уведомлений
    const addNotification = (message) => {
        const now = new Date();
        const time = now.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
        const newNotification = { message, time };
        setNotifications(prev => [newNotification, ...prev].slice(0, 10)); // Ограничение до 10 уведомлений
    };

    const toggleLED2 = () => {
    const newState = !led2State; // Новое состояние переключателя
    fetch('/api/toggle-module/RGBLenta_Bedroom', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            // Проверяем, что пришел ответ с актуальным состоянием устройства
            if (data.State_of_Lamp_Bedroom !== undefined) {
                const actualState = data.State_of_Lamp_Bedroom === "true"; // Преобразуем строку в булево значение
                setLed2State(actualState); // Обновляем состояние на фронте
            } else {
                console.error("Некорректный ответ от сервера:", data);
                setLed2State(newState); // Откат состояния в случае ошибки
            }
        })
        .catch(err => {
            console.error("Ошибка переключения лампы:", err);
            setLed2State(newState); // Откат состояния в случае ошибки
        });
    };


    const toggleFan = () => {
    const newState = !fanState; // Новое состояние переключателя (переключаемся на противоположное)
    fetch('/api/toggle-module/powerVentilation', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            // Проверяем, что пришел ответ с актуальным состоянием устройства
            if (data.State_of_Ventilation !== undefined) {
                const actualState = data.State_of_Ventilation === "true"; // Преобразуем строку в булево значение
                setFanState(actualState); // Обновляем состояние фронта
            } else {
                console.error("Некорректный ответ от сервера:", data);
                setFanState(newState); // Откат состояния в случае ошибки
            }
        })
        .catch(err => {
            console.error("Ошибка переключения вентилятора:", err);
            setFanState(newState); // Откат состояния в случае ошибки
        });
    };

    const toggleKlimatFan = () => {
    const newState = !klimatFanState; // Новое состояние переключателя (переключаемся на противоположное)
    fetch('/api/toggle-module/Klimat_Kontrol', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            // Проверяем, что пришел ответ с актуальным состоянием устройства
            if (data.State_of_Klimat_Kontrol !== undefined) {
                const actualState = data.State_of_Klimat_Kontrol === "true"; // Преобразуем строку в булево значение
                setKlimatFanState(actualState); // Обновляем состояние фронта
            } else {
                console.error("Некорректный ответ от сервера:", data);
                setKlimatFanState(newState); // Откат состояния в случае ошибки
            }
        })
        .catch(err => {
            console.error("Ошибка переключения вентилятора:", err);
            setKlimatFanState(newState); // Откат состояния в случае ошибки
        });
    };

    const setFanThresholdValue = () => {
        const threshold = document.getElementById('fanThresholdInput').value;
        fetch('/api/toggle-module/fanThreshold', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ threshold }),
        })
            .then(response => response.text())
            .then(text => {
                alert(text);
                setFanThreshold(threshold);
            })
            .catch(err => console.error("Ошибка установки порога вентилятора:", err));
    };

    const toggleAutoMode = () => {
        fetch('/api/toggle-module/autoMode', { method: 'POST' })
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
                    led2State={led2State}
                    toggleLED2={toggleLED2}
                />
            )}
            {activeTab === 'Sensors' && (
                <Sensors
                    motion={motion}
                    smoke={smoke}
		    protechka={protechka}
                    notifications={notifications}
                />
            )}
        </div>
    );
};

export default App;