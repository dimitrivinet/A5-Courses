#define EPS 0.001
#define MAX_STEPS 100
#define SURF_THRESHOLD 0.001
#define FXAA 1

struct PinholeCamera {
    vec3 pos, dir;
    float fov;
};

struct Ray {
    vec3 origin, dir;
};

struct LightSource {
    vec3 dir, color;
    float intensity;
};

struct Material {
    vec3 color;
};

struct Hit {
    vec3 point;
    float dist;
    Material mat;
};

const Material planetMat = Material(vec3(0.85, 0.37, 0.09));
const Material moonMat = Material(vec3(0.88));

mat3 computeViewMatrix(PinholeCamera cam) {
    vec3 cw = normalize(cam.dir);
    vec3 cr = vec3(0.0, 1.0, 0.0);
    vec3 cu = normalize(cross(cw, cr));
    vec3 cv = normalize(cross(cu, cw));

    return mat3(cu, cv, cw);
}

float sdf_circle(vec2 p, float r) {
    return length(p) - r;
}

float sdf_sphere(vec3 p, float r) {
    return length(p) - r;
}

Hit sdf_scene(vec3 p) {
    vec3 planetP = p + 0.5 * vec3(cos(iTime), sin(iTime), 0.0);
    vec3 moonP = planetP + 1.0 * vec3(sin(iTime), 0.0, cos(iTime));

    float planet = sdf_sphere(planetP, 0.5);
    float moon = sdf_sphere(moonP, 0.1);

    float planetNoise = texture(iChannel0, planetP.xy).y / 80.0;
    float moonNoise = texture(iChannel0, moonP.xy).y / 80.0;

    if(planet < moon)
        return Hit(vec3(0.0), planet + planetNoise, planetMat);
    else
        return Hit(vec3(0.0), moon + moonNoise, moonMat);
}

Hit raymarch(Ray ray) {
    int step = 0;
    float totalDist = 0.0;
    vec3 ray_pos;
    Hit hit;

    while(step < MAX_STEPS) {
        ray_pos = ray.origin + totalDist * ray.dir;
        hit = sdf_scene(ray_pos);

        if(hit.dist < SURF_THRESHOLD)
            return Hit(ray_pos, totalDist, hit.mat);
        totalDist += hit.dist;

        step += 1;
    }
    return Hit(vec3(0.0), -1.0, Material(vec3(0.0)));;
}

vec3 computeNormals(vec3 p) {
    vec2 eps = vec2(EPS, 0.0);
    float t = sdf_scene(p).dist;
    return normalize(vec3(t - sdf_scene(p - eps.xyy).dist, t - sdf_scene(p - eps.yxy).dist, t - sdf_scene(p - eps.yyx).dist));
}

vec3 render(Ray ray) {
    Hit hit = raymarch(ray);


    vec3 collision = ray.origin + hit.dist * ray.dir;
    vec3 n = computeNormals(collision);

    vec3 keyLightDir = normalize(vec3(-0.5, 0.5, -0.5));
    vec3 keyLightColor = vec3(1);
    float keyLightIntensity = 1.0;
    LightSource keyLight = LightSource(keyLightDir, keyLightColor, keyLightIntensity);
    vec3 key = dot(n, keyLight.dir) * keyLight.intensity * keyLight.color;

    vec3 fillLightDir = vec3(0.2, 0.5, 0.8);
    vec3 fillLightColor = vec3(0, 1, 0.5);
    float fillLightIntensity = 0.1;
    LightSource fillLight = LightSource(fillLightDir, fillLightColor, fillLightIntensity);
    vec3 fill = dot(n, fillLight.dir) * fillLight.intensity * fillLight.color;

    vec3 backLightDir = normalize(vec3(0.0, 0.0, -1));
    vec3 backLightColor = vec3(0.49, 0.67, 0.72);
    float backLightIntensity = 0.2;
    LightSource backLight = LightSource(backLightDir, backLightColor, backLightIntensity);
    vec3 back = dot(n, backLight.dir) * backLight.intensity * backLight.color;

    vec3 col = max(key, 0.0) + max(fill, 0.0) + max(back, 0.0) + 0.1 * fillLight.color;

    col = hit.dist >= 0.0 ? col * hit.mat.color : backLight.color;
    col = pow(col, vec3(1.0 / 2.2));

    return col;
}

float n21 (vec2 p) {
    return fract(sin(p.x * 12.9898 + p.y * 78.233) + 43758.5453);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    float aspectRatio = iResolution.x / iResolution.y;

    vec2 uvInit = fragCoord / iResolution.xy;
    vec2 uv = 2.0 * (uvInit - 0.5);
    uv.x *= aspectRatio;

    vec3 cam_pos = vec3(0.0, 0.0, -2.0);
    vec3 cam_dir = vec3(0.0, 0.0, 1.0);
    float cam_fov = 65.0;
    PinholeCamera cam = PinholeCamera(cam_pos, cam_dir, cam_fov);

    mat3 view = computeViewMatrix(cam);

    vec3 ray_ori = cam.pos;

    vec3 col;
    for(int i = 0; i < FXAA; ++i) {
        for(int j = 0; j < FXAA; ++j) {
            vec2 offset = vec2(n21(vec2(i, i)) * EPS, n21(vec2(j, j)) * EPS);
            vec3 ray_dir = view * normalize(vec3(uv + offset, 1.0));
            Ray ray = Ray(ray_ori, ray_dir);

            col = render(ray);
        }
    }

    // Output to screen
    fragColor = vec4(col, 1.0);
}
