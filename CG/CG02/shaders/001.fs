#define EPS .01

vec3 square(vec2 p, float coeff) {
    float vx = max(1. - abs(p.x), 0.);
    float vy = max(1. - abs(p.y), 0.);
    vec3 col = vec3(coeff * vx * vy);

    return col;
}

float peas(vec2 p, float rad, float circleSpeed) {
    float radius = sin(circleSpeed * iTime) * .1;

    p = p.xy;
    p = mod(p, rad * 2.) - rad;

    float s = length(p - vec2(0.)) - .1;
    s = smoothstep(radius, radius + EPS, s);

    return s;
}

float n21(vec2 t) {
    return fract(sin(t.x * 12.02964 + t.y * 91.2095) * 302958.35024);
}

float peas_noise(vec2 p, float rad, float circleSpeed) {
    vec2 v = mod(p, rad * 2.) - rad;
    vec2 i = floor(p.xy / (2. * rad));

    float n = n21(i) * 192.304;
    float radius = rad * (.5 + .5 * sin(circleSpeed * iTime + n));

    float s = length(v - .0) - radius;
    s = smoothstep(0., EPS, s + EPS / 2.);

    return s;
}

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    float aspectRatio = iResolution.x / iResolution.y;

    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = fragCoord / iResolution.xy;
    uv = 2. * (uv - .5);
    uv.x = uv.x * aspectRatio;

    // vec3 col = square(uv, 10000000.);

    // float s = peas(uv, .5, 5.);
    // vec3 col = vec3(s, s, 1.);

    // float random = n21(uv * mod(iTime, 100.));
    // vec3 col = vec3(random);

    // vec2 v = mod(uv, vec2(.2));
    // vec2 i = floor(uv / vec2(.2));
    // vec3 col = vec3(n21(i));

    vec3 col = vec3(peas_noise(uv, .1, 1.));

    // Output to screen
    fragColor = vec4(col, 1.0);
}
