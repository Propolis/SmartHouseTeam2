import React from 'react';

function Sensors({ motion, smoke, protechka, pompaState, togglePompa, notifications }) {
    return (
        <div className="tabcontent">
            <h2>Датчики</h2>
            <div className="sensor-tile">
                <h3>Движение</h3>
                <p><span id="motion">{motion}</span></p>
            </div>
            <div className="sensor-tile">
                <h3>Газ</h3>
                <p><span id="smoke">{smoke}</span></p>
            </div>
	    <div className="sensor-tile">
                <h3>Протечка</h3>
                <p><span id="protechka">{protechka}</span></p>
            </div>
	    <div className="sensor-tile">
                <h3>Подача воды</h3>
		<label className="switch">
                    <input
                        type="checkbox"
                        id="pompaSwitch"
                        checked={pompaState}
                        onChange={togglePompa}
                    />
                    <span className="slider"></span>
                </label>
            </div>
            <div className="notifications">
                <h3>Уведомления</h3>
                <div id="notifications">
                    {notifications.length === 0 ? (
                        <div className="notification">Уведомлений нет</div>
                    ) : (
                        notifications.map((notification, index) => (
                            <div key={index} className="notification">
                                <strong>{notification.time}</strong>: {notification.message}
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}

export default Sensors;