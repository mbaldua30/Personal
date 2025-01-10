// Example Data (This will be injected by Flask in a real-world scenario)
const carData = {{ car_data | tojson }};  // Passing the data from Flask to JavaScript

// Update Model options based on the selected Make
function updateModelOptions() {
    const makeSelect = document.getElementById('makeSelect');
    const modelSelect = document.getElementById('modelSelect');
    const selectedMake = makeSelect.value;

    // Clear previous options
    modelSelect.innerHTML = '<option value="">Select Model</option>';
    modelSelect.disabled = !selectedMake;

    // If a make is selected, populate models
    if (selectedMake) {
        const models = Object.keys(carData[selectedMake]);
        models.forEach(model => {
            const option = document.createElement('option');
            option.value = model;
            option.textContent = model;
            modelSelect.appendChild(option);
        });
    }
    updateVariantOptions(); // Reset variant options when make is changed
}

// Update Variant options based on the selected Model
function updateVariantOptions() {
    const makeSelect = document.getElementById('makeSelect');
    const modelSelect = document.getElementById('modelSelect');
    const variantSelect = document.getElementById('variantSelect');
    const selectedMake = makeSelect.value;
    const selectedModel = modelSelect.value;

    // Clear previous options
    variantSelect.innerHTML = '<option value="">Select Variant</option>';
    variantSelect.disabled = !(selectedMake && selectedModel);

    // If a model is selected, populate variants
    if (selectedMake && selectedModel) {
        const variants = Object.keys(carData[selectedMake][selectedModel]);
        variants.forEach(variant => {
            const option = document.createElement('option');
            option.value = variant;
            option.textContent = variant;
            variantSelect.appendChild(option);
        });
    }
    updateAccessoryOptions(); // Reset accessory options when variant is changed
}

// Update Accessory options based on the selected Variant
function updateAccessoryOptions() {
    const makeSelect = document.getElementById('makeSelect');
    const modelSelect = document.getElementById('modelSelect');
    const variantSelect = document.getElementById('variantSelect');
    const accessorySelect = document.getElementById('accessorySelect');
    const selectedMake = makeSelect.value;
    const selectedModel = modelSelect.value;
    const selectedVariant = variantSelect.value;

    // Clear previous options
    accessorySelect.innerHTML = '<option value="">Select Accessory</option>';
    accessorySelect.disabled = !(selectedMake && selectedModel && selectedVariant);

    // If a variant is selected, populate accessories
    if (selectedMake && selectedModel && selectedVariant) {
        const accessories = carData[selectedMake][selectedModel][selectedVariant];
        accessories.forEach(accessory => {
            const option = document.createElement('option');
            option.value = accessory.accessory;
            option.textContent = accessory.accessory;
            accessorySelect.appendChild(option);
        });
    }
    updateColorOptions(); // Reset color options when accessory is changed
}

// Update Color options based on the selected Accessory
function updateColorOptions() {
    const colorSelect = document.getElementById('colorSelect');
    const accessorySelect = document.getElementById('accessorySelect');
    const selectedAccessory = accessorySelect.value;

    // Clear previous options
    colorSelect.innerHTML = '<option value="">Select Color</option>';
    colorSelect.disabled = !selectedAccessory;

    // If an accessory is selected, populate color options
    if (selectedAccessory) {
        const colors = ['Red', 'Blue', 'Black', 'White']; // Example colors for demonstration
        colors.forEach(color => {
            const option = document.createElement('option');
            option.value = color;
            option.textContent = color;
            colorSelect.appendChild(option);
        });
    }
}
