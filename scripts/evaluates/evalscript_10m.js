//VERSION=3
function setup() {
    return {
        input: ["B02", "B03", "B04", "B08"],
        output: {bands: 4, sampleType: "FLOAT32"}
    };
}

function evaluatePixel(sample) {
    return [sample.B02, sample.B03, sample.B04, sample.B08];
}
