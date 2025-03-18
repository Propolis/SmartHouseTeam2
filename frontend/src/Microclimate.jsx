import React from 'react';

function Microclimate({ temperature, humidity, bathHumidity, fanThreshold, bathFanThreshold, autoMode, bathAutoMode, fanState, toggleFan, klimatFanState, toggleKlimatFan, setFanThresholdValue, setBathFanThresholdValue, toggleAutoMode, toggleBathAutoMode }) {
    return (
        <div className="tabcontent">
            <h2>Микроклимат в жилых помещениях</h2>
            <div className="data-tile">
                <h3>Температура</h3>
                <p id="temperature">{temperature}°C</p>
            </div>
            <div className="data-tile">
                <h3>Влажность</h3>
                <p id="humidity">{humidity} %</p>
            </div>
            <h2>Управление кондиционером</h2>
            <div className="fan-tile">
                <img src="https://cdn-icons-png.flaticon.com/512/8866/8866925.png" alt="Кондиционер" />
                <h3>Кондиционер</h3>
                <label className="switch">
                    <input
                        type="checkbox"
                        id="klimatFanSwitch"
                        checked={klimatFanState}
                        onChange={toggleKlimatFan}
                    />
                    <span className="slider"></span>
                </label>
            </div>

            <div className="flex-row">
                <p>Порог температуры: <span id="fanThreshold">{fanThreshold}°C</span></p>
                <input type="number" id="fanThresholdInput" placeholder="Введите порог" />
                <button onClick={setFanThresholdValue}>Установить</button>
            </div>
            <div className="flex-row">
                <p>Режим управления: <span id="autoMode">{autoMode ? 'Автоматический' : 'Ручной'}</span></p>
                <button onClick={toggleAutoMode}>Переключить режим</button>
            </div>
	    <h2>Микроклимат в ванной</h2>
            <div className="fan-tile">
                <img src="https://cdn-icons-png.flaticon.com/512/979/979619.png" alt="Вентиляция" />
                <h3>Вентиляция</h3>
                <label className="switch">
                    <input
                        type="checkbox"
                        id="fanSwitch"
                        checked={fanState}
                        onChange={toggleFan}
                    />
                    <span className="slider"></span>
                </label>
            </div>
            <div className="data-tile">
		<h3>Влажность</h3>
                <p id="bathHumidity">{bathHumidity}%</p>
            </div>
            <div className="flex-row">
                <p>Порог влажности: <span id="bathFanThreshold">{bathFanThreshold}%</span></p>
                <input type="number" id="bathFanThresholdInput" placeholder="Введите порог" />
                <button onClick={setBathFanThresholdValue}>Установить</button>
            </div>
            <div className="flex-row">
                <p>Режим управления: <span id="bathAutoMode">{bathAutoMode ? 'Автоматический' : 'Ручной'}</span></p>
                <button onClick={toggleBathAutoMode}>Переключить режим</button>
            </div>
        </div>
    );
}

export default Microclimate;