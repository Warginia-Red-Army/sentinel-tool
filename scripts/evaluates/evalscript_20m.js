//VERSION=3
function setup() {
    return {
        input: ["B05", "B06", "B07", "B8A", "B11", "B12"],
        output: {bands: 6, sampleType: "FLOAT32"}
    };
}

function evaluatePixel(sample) {
    return [sample.B05, sample.B06, sample.B07, sample.B8A, sample.B11, sample.B12];
}