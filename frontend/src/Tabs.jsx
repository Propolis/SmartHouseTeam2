import React from 'react';

function Tabs({ activeTab, setActiveTab }) {
    return (
        <div className="tab">
            <button className={`tablinks ${activeTab === 'Microclimate' ? 'active' : ''}`} onClick={() => setActiveTab('Microclimate')}>
                Микроклимат
            </button>
            <button className={`tablinks ${activeTab === 'Lighting' ? 'active' : ''}`} onClick={() => setActiveTab('Lighting')}>
                Освещение
            </button>
            <button className={`tablinks ${activeTab === 'Sensors' ? 'active' : ''}`} onClick={() => setActiveTab('Sensors')}>
                Датчики
            </button>
        </div>
    );
}

export default Tabs;