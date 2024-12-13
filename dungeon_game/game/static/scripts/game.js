const DungeonGame = {
    elements: {
        dungeonGrid: document.getElementById('dungeon-grid'),
        minHealthSpan: document.getElementById('min-health'),
        newGameBtn: document.getElementById('new-game-btn'),
        cellLegend: document.getElementById('cell-legend')
    },

    init() {
        this.elements.newGameBtn.addEventListener('click', this.generateDungeon.bind(this));
        this.generateDungeon();
        
    },

    generateDungeon() {
        axios.get('/generate-dungeon/')
        .then(response => this.renderDungeon(response.data))
            .then(data => this.calculateHealth(data.dungeon))
            .catch(this.handleError);
        this.populateLegend();
    },
    renderDungeon({ dungeon_details, rows, cols }) {
        // Set grid columns dynamically
        this.elements.dungeonGrid.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
        this.elements.dungeonGrid.innerHTML = '';

        dungeon_details.forEach(row => row.forEach(this.createCell.bind(this)));
    },
    createCell(cellData) {
        const cellElement = document.createElement('div');
        cellElement.classList.add('cell-item', 'border', 'rounded', 'overflow-hidden', 'shadow-lg');

        const img = document.createElement('img');
        img.src = `/static/image/${cellData.image}`;
        img.alt = cellData.type;
        img.classList.add('cell-image');
        cellElement.appendChild(img);

        const damageSpan = document.createElement('span');
        damageSpan.textContent = cellData.damage;
        damageSpan.classList.add('cell-damage');
        cellElement.appendChild(damageSpan);

        this.elements.dungeonGrid.appendChild(cellElement);
    },
    calculateHealth(dungeon) {
        return axios.post('/calculate-minimum-health/', { dungeon }, {
            headers: { 'X-CSRFToken': document.querySelector('[name=csrf-token]').content }
        })
        .then(healthResponse => {
            this.elements.minHealthSpan.textContent = healthResponse.data.minimum_health;
        })
        .catch(this.handleError);
    },
    handleError(error) {
        console.error('Dungeon generation error:', error);
        this.elements.minHealthSpan.textContent = 'Error';
    },
    populateLegend() {
        axios.get('/generate-dungeon/')
            .then(response => {
                const seenItem = new Set();
                response.data.dungeon_details[0].forEach(cellType => {
                    if (!seenItem.has(cellType.type)) {
                        seenItem.add(cellType.type);
                        this.createLegendItem(cellType);
                    }
                });
            });
    },
    createLegendItem(cellType) {
        const legendItem = document.createElement('div');
        legendItem.classList.add('legend-item');

        const img = document.createElement('img');
        img.src = `/static/image/${cellType.image}`;
        img.alt = cellType.type;
        img.classList.add('cell-legend-image');

        const textDiv = document.createElement('div');
        textDiv.innerHTML = `<strong>${cellType.type.charAt(0).toUpperCase() + cellType.type.slice(1)}</strong>`;

        legendItem.appendChild(img);
        legendItem.appendChild(textDiv);
        this.elements.cellLegend.appendChild(legendItem);
    }
};

// Initialize the game
DungeonGame.init();