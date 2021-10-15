#define EPS               .01
#define BASE_BALL_POS    1.
#define CAM_POS         -2.
#define PLANET_RADIUS     .05

// to get background texture run this in dev console:
// gShaderToy.SetTexture(0, {mSrc:'https://live.staticflickr.com/1354/5119773924_13f7eaedfa_b.jpg', mType:'texture', mID:1, mSampler:{ filter: 'mipmap', wrap: 'repeat', vflip:'true', srgb:'false', internal:'byte' }});

vec4 planets[5] = vec4[] (vec4(-0.02, 0.03, 0., .1), vec4(2., 2., .6, .04), vec4(.5, 1., 1.3, .2), vec4(3., .7, .2, .1), vec4(.3, .3, 0., .05));

vec3 planetOffsets[5] = vec3[] (vec3(0.), vec3(1.), vec3(-0.2), vec3(0.), vec3(0.));

vec3 planetColors[5] = vec3[] (vec3(1., 1., 0.), vec3(.3, .6, .9), vec3(.1, .8, .3), vec3(.9, .8, .7), vec3(.8, .4, .2));

float distLine(vec3 ro, vec3 rd, vec3 p) {
    return length(cross(p - ro, rd)) / length(rd);
}

vec3 planet(vec3 ro, vec3 rd, float planetSize, vec3 orbit, vec3 orbitOffset, vec3 planetColors) {

    float t = iTime;
    vec3 p = vec3(orbit.x * sin(t) + orbitOffset.x, orbit.y * cos(t) + orbitOffset.y, BASE_BALL_POS + orbit.z * sin(t) + orbitOffset.z);

    float d = distLine(ro, rd, p);

    d = smoothstep(planetSize, planetSize - 0.004, d);

    return d * planetColors;
}

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    float aspectRatio = iResolution.x / iResolution.y;

    // Normalized pixel coordinates (from 0 to 1)
    vec2 uvInit = fragCoord / iResolution.xy;
    vec2 uv = 2. * (uvInit - .5);
    uv.x = uv.x * aspectRatio;

    vec3 ro = vec3(0., 0., CAM_POS);
    vec3 rd = vec3(uv.x, uv.y, 0.) - ro;

    vec3 d = vec3(.5);

    for(int i = 0; i < 5; ++i) {
        d = planet(ro, rd, planets[i].w, planets[i].xyz, planetOffsets[i], planetColors[i]);
        if(d != vec3(0.)) {
            break;
        }
        d = texture(iChannel0, uvInit).xyz * .5;
    }

    vec3 col = d;

    // Output to screen
    fragColor = vec4(col, 1.0);
}
