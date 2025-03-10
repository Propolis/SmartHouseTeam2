// Lighting.jsx
import React from 'react';

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

export default Lighting;
