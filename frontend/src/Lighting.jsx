import React from 'react';

function Lighting({
    led2State,
    toggleLED2,
    lampColor, 
    toggleLampColor 
}) {
    return (
        <div className="tabcontent">
            <h2>Управление освещением</h2>
            <div className="light-tile">
                <img src="https://cdn-icons-png.flaticon.com/512/702/702814.png" alt="Лампочка" />
                <h3>Спальня</h3>
                <p>Свет</p>
                <label className="switch">
                    <input
                        type="checkbox"
                        id="led2Switch"
                        checked={led2State}
                        onChange={toggleLED2}
                    />
                    <span className="slider"></span>
                </label>
		<p>
		    <input
                        type="color"
                        value={lampColor}
                        onChange={(e) => toggleLampColor(e.target.value)}
                        style={{ width: '60px', height: '30px' }}
                    />
		</p>
            </div>
        </div>
    );
}

export default Lighting;