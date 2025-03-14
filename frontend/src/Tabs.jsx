// Tabs.jsx
import React, { useState } from 'react';
import Microclimate from './Microclimate';
import Lighting from './Lighting';
import Sensors from './Sensors';

const Tabs = (props) => {
    const {
        motion, smoke, notifications,
        temperature, humidity, fanThreshold, autoMode, fanState,
        toggleFan, setFanThresholdValue, toggleAutoMode,
        led1State, led2State, toggleLED1, toggleLED2
    } = props;

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
            </div>
            <div className="tabcontent" style={{ display: activeTab === 'Lighting' ? 'block' : 'none' }}>
                <Lighting
                    led1State={led1State}
                    led2State={led2State}
                    toggleLED1={toggleLED1}
                    toggleLED2={toggleLED2}
                />
            </div>
            <div className="tabcontent" style={{ display: activeTab === 'Sensors' ? 'block' : 'none' }}>
                <Sensors
                    motion={motion}
                    smoke={smoke}
                    notifications={notifications}
                />
            </div>
        </div>
    );
};

export default Tabs;
