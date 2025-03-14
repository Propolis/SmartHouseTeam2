// Sensors.jsx
import React from 'react';

const Sensors = ({ motion, smoke, notifications }) => {
    return (
        <div>
            <h2>Датчики</h2>
            <p>Движение: {motion}</p>
            <p>Дым: {smoke}</p>
            <div className="notifications">
                <h3>Уведомления</h3>
                <div id="notifications">
                    {notifications && notifications.map((notification, index) => (
                        <div key={index} className="notification">
                            <strong>{notification.time}</strong>: {notification.message}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Sensors;
