import streamlit as st
import pandas as pd
import folium
import streamlit.components.v1 as components

from streamlit_folium import st_folium
# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Space Analog Finder",
    page_icon="🚀",
    layout="wide"
)
# ==========================================
# SPACE ANALOG FINDER - SOLAR SYSTEM ANIMATION
# ==========================================

components.html("""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    overflow: hidden;
    background: #01030b;
}

/* =========================================
   CINEMATIC DEEP SPACE BACKGROUND
========================================= */

.space {
    position: relative;
    width: 100%;
    height: 520px;
    overflow: hidden;
    isolation: isolate;

    background:
        radial-gradient(ellipse at 15% 20%,
            rgba(93, 39, 145, .30), transparent 42%),

        radial-gradient(ellipse at 75% 15%,
            rgba(38, 75, 155, .25), transparent 45%),

        radial-gradient(ellipse at 48% 75%,
            rgba(100, 35, 100, .19), transparent 42%),

        radial-gradient(ellipse at 90% 75%,
            rgba(20, 70, 125, .20), transparent 40%),

        linear-gradient(
            145deg,
            #01020a 0%,
            #05091b 45%,
            #08051b 75%,
            #01030a 100%
        );
}

/* Layered nebula clouds */
.nebula {
    position: absolute;
    inset: -35%;
    z-index: 0;
    pointer-events: none;

    background:
        radial-gradient(ellipse at 20% 35%,
            rgba(118, 60, 190, .34), transparent 22%),

        radial-gradient(ellipse at 35% 45%,
            rgba(190, 65, 150, .22), transparent 25%),

        radial-gradient(ellipse at 48% 25%,
            rgba(55, 95, 200, .25), transparent 27%),

        radial-gradient(ellipse at 65% 55%,
            rgba(75, 45, 155, .25), transparent 30%),

        radial-gradient(ellipse at 80% 25%,
            rgba(40, 110, 180, .20), transparent 25%),

        radial-gradient(ellipse at 30% 75%,
            rgba(175, 55, 105, .15), transparent 25%);

    filter: blur(38px);

    animation: cosmicNebula 100s ease-in-out infinite alternate;
}

@keyframes cosmicNebula {
    0% {
        transform: translate(-2%, 1%) scale(1);
    }

    50% {
        transform: translate(1%, -1%) scale(1.05);
    }

    100% {
        transform: translate(3%, 2%) scale(1.1);
    }
}

/* Galactic dust / Milky Way band */
.space::before {
    content: "";
    position: absolute;
    z-index: 0;
    inset: -50%;

    background:
        radial-gradient(
            ellipse at center,
            rgba(150, 160, 220, .12),
            rgba(90, 100, 180, .07) 22%,
            transparent 55%
        );

    transform: rotate(-24deg) scaleY(.35);

    filter: blur(20px);

    animation: galaxyDrift 120s linear infinite alternate;

    pointer-events: none;
}

@keyframes galaxyDrift {
    from {
        transform: rotate(-24deg) translateX(-2%) scaleY(.35);
    }

    to {
        transform: rotate(-24deg) translateX(3%) scaleY(.42);
    }
}

/* Fine cosmic haze */
.space::after {
    content: "";
    position: absolute;
    inset: 0;
    z-index: 0;
    pointer-events: none;

    background:
        radial-gradient(circle at 50% 45%,
            transparent 25%,
            rgba(0, 0, 12, .35) 100%);
}

/* Star canvas */
#stars {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    pointer-events: none;
}
/* STARS */
#stars {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    pointer-events: none;
}

/* SHOOTING STARS */
.shooting {
    position: absolute;
    width: 130px;
    height: 2px;
    background: linear-gradient(90deg, white, rgba(120,180,255,.5), transparent);
    box-shadow: 0 0 8px #8bcaff;
    transform: rotate(-35deg);
    opacity: 0;
    z-index: 3;
    animation: shooting 12s linear infinite;
}

.shooting.one {
    top: 15%;
    left: 80%;
    animation-delay: 1s;
}

.shooting.two {
    top: 40%;
    left: 60%;
    animation-delay: 7s;
}

.shooting.three {
    top: 65%;
    left: 35%;
    animation-delay: 10s;
}

@keyframes shooting {
    0% {
        opacity: 0;
        transform: translate(0,0) rotate(-35deg);
    }
    3% { opacity: 1; }
    12% {
        opacity: 0;
        transform: translate(-240px,150px) rotate(-35deg);
    }
    100% { opacity: 0; }
}

/* TITLE */
.title {
    position: absolute;
    z-index: 10;
    top: 25px;
    left: 30px;
    color: white;
    font-family: Arial, sans-serif;
    font-size: clamp(22px,4vw,35px);
    font-weight: 800;
    letter-spacing: 4px;
    text-shadow: 0 0 20px rgba(120,170,255,.9);
}

.subtitle {
    position: absolute;
    z-index: 10;
    top: 70px;
    left: 33px;
    color: #c6d5f5;
    font-family: Arial, sans-serif;
    font-size: 10px;
    letter-spacing: 2.5px;
}

/* THREE.JS */
#planetScene {
    position: absolute;
    inset: 0;
    z-index: 2;
}

/* PLANET LABELS */
.planet-label {
    position: absolute;
    z-index: 8;
    color: #eaf2ff;
    font-family: Arial, sans-serif;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 2px;
    text-shadow: 0 0 10px #65aaff, 0 0 20px #317cff;
    pointer-events: none;
    white-space: nowrap;
    transform: translate(-50%, 0);
}

</style>
</head>

<body>

<div class="space">

    <div class="nebula"></div>

    <canvas id="stars"></canvas>

    <div class="shooting one"></div>
    <div class="shooting two"></div>
    <div class="shooting three"></div>

    <div class="title">SPACE ANALOG FINDER</div>

    <div class="subtitle">
        EXPLORING EARTH ANALOGUES FOR MOON & MARS HABITATS
    </div>

    <div id="planetScene"></div>

    <div id="moonLabel" class="planet-label">MOON</div>
    <div id="marsLabel" class="planet-label">MARS</div>

</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script>

const container = document.getElementById("planetScene");

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
    42,
    container.clientWidth / container.clientHeight,
    0.1,
    1000
);

camera.position.set(0, 0, 12);

const renderer = new THREE.WebGLRenderer({
    alpha: true,
    antialias: true
});

renderer.setSize(
    container.clientWidth,
    container.clientHeight
);

renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

renderer.outputEncoding = THREE.sRGBEncoding;

container.appendChild(renderer.domElement);


// =====================================
// LIGHTING
// =====================================

const sunlight = new THREE.DirectionalLight(0xffffff, 1.35);

sunlight.position.set(-5, 5, 8);

scene.add(sunlight);

const blueLight = new THREE.PointLight(0x367cff, 1.5, 25);

blueLight.position.set(5, 2, 5);

scene.add(blueLight);

scene.add(new THREE.AmbientLight(0x506b9c, 0.55));


// =====================================
// EARTH
// =====================================

const earthGroup = new THREE.Group();

earthGroup.position.set(2.1, -4.0, -1.5);

scene.add(earthGroup);

const loader = new THREE.TextureLoader();

loader.setCrossOrigin("anonymous");

let earthMesh;

loader.load(
    "https://threejs.org/examples/textures/planets/earth_atmos_2048.jpg",

    function(texture) {

        texture.encoding = THREE.sRGBEncoding;

        const geometry = new THREE.SphereGeometry(4.5, 128, 128);

        const material = new THREE.MeshPhongMaterial({

            map: texture,

            // Boost the blue ocean appearance
            color: new THREE.Color(0x75a9e8),

            shininess: 22,

            specular: new THREE.Color(0x254f91)

        });

        earthMesh = new THREE.Mesh(geometry, material);

        earthGroup.add(earthMesh);

    },

    undefined,

    function(error) {
        console.error("Earth texture loading failed", error);
    }
);


// =====================================
// EARTH ATMOSPHERE
// =====================================

const atmosphereGeometry = new THREE.SphereGeometry(4.62, 128, 128);

const atmosphereMaterial = new THREE.ShaderMaterial({

    transparent: true,

    side: THREE.BackSide,

    vertexShader: `
        varying vec3 vNormal;

        void main() {
            vNormal = normalize(normalMatrix * normal);

            gl_Position = projectionMatrix *
                          modelViewMatrix *
                          vec4(position, 1.0);
        }
    `,

    fragmentShader: `
        varying vec3 vNormal;

        void main() {

            float intensity =
                pow(0.72 - dot(vNormal, vec3(0.0,0.0,1.0)), 3.0);

            gl_FragColor = vec4(
                0.10,
                0.42,
                1.0,
                intensity * 0.9
            );
        }
    `

});

const atmosphere = new THREE.Mesh(
    atmosphereGeometry,
    atmosphereMaterial
);

earthGroup.add(atmosphere);


// =====================================
// EARTH CLOUD LAYER
// =====================================

loader.load(
    "https://threejs.org/examples/textures/planets/earth_clouds_1024.png",

    function(texture) {

        const cloudGeometry = new THREE.SphereGeometry(
            4.54, 128, 128
        );

        const cloudMaterial = new THREE.MeshPhongMaterial({

            map: texture,

            transparent: true,

            opacity: 0.22,

            depthWrite: false

        });

        const clouds = new THREE.Mesh(
            cloudGeometry,
            cloudMaterial
        );

        earthGroup.add(clouds);

        clouds.userData.isCloud = true;

    },

    undefined,

    function() {
        console.log("Cloud texture unavailable; Earth surface remains visible.");
    }
);


// =====================================
// MOON WITH CRATERS
// =====================================

// =====================================
// REALISTIC MOON - HIGH DETAIL
// =====================================

const moonGroup = new THREE.Group();

moonGroup.position.set(2.0, 1.7, 0.5);

scene.add(moonGroup);


// Load realistic lunar surface texture
loader.load(
    "https://threejs.org/examples/textures/planets/moon_1024.jpg",

    function(moonTexture) {

        moonTexture.encoding = THREE.sRGBEncoding;

        const moonGeometry = new THREE.SphereGeometry(
            0.43,
            128,
            128
        );

        const moonMaterial = new THREE.MeshStandardMaterial({

            map: moonTexture,

            bumpMap: moonTexture,

            bumpScale: 0.045,

            color: 0xd0d0d0,

            roughness: 1.0,

            metalness: 0.0

        });

        const moon = new THREE.Mesh(
            moonGeometry,
            moonMaterial
        );

        moonGroup.add(moon);

    },

    undefined,

    function(error) {
        console.error("Moon texture could not load:", error);
    }
);


// Realistic lunar lighting
const moonLight = new THREE.DirectionalLight(
    0xffffff,
    1.4
);

moonLight.position.set(-4, 4, 6);

scene.add(moonLight);


// Subtle blue space reflection
const moonReflection = new THREE.PointLight(
    0x829acb,
    0.25,
    4
);

moonReflection.position.set(2, 1.7, 1);

scene.add(moonReflection);


// =====================================
// MARS
// =====================================

const marsGroup = new THREE.Group();

marsGroup.position.set(-0.9, 0.8, 0.3);

scene.add(marsGroup);

const mars = new THREE.Mesh(

    new THREE.SphereGeometry(0.25, 64, 64),

    new THREE.MeshStandardMaterial({

        color: 0xb84b2c,

        roughness: 1

    })

);

marsGroup.add(mars);


// =====================================
// LABELS FOLLOW THE PLANETS
// =====================================

const moonLabel = document.getElementById("moonLabel");

const marsLabel = document.getElementById("marsLabel");

function updateLabel(object, label) {

    const position = object.position.clone();

    position.project(camera);

    const x = (position.x * 0.5 + 0.5) * container.clientWidth;

    const y = (-position.y * 0.5 + 0.5) * container.clientHeight;

    label.style.left = x + "px";

    label.style.top = (y + 32) + "px";

    label.style.display =
        position.z < 1 ? "block" : "none";
}


// =====================================
// ANIMATION
// =====================================

const clock = new THREE.Clock();

function animate() {

    requestAnimationFrame(animate);

    const time = clock.getElapsedTime();

    // Extremely slow Earth rotation
    earthGroup.rotation.y = time * 0.012;

    // Slight cloud movement
    earthGroup.children.forEach(child => {

        if (child.userData.isCloud) {
            child.rotation.y = time * 0.016;
        }

    });

    // Gentle Moon movement
    moonGroup.position.y =
        1.7 + Math.sin(time * 0.22) * 0.045;
        
    // Slow realistic Moon rotation
    moonGroup.rotation.y += 0.00025;
    moonGroup.rotation.x = 0.04;

    moonGroup.position.x =
        2.0 + Math.sin(time * 0.12) * 0.06;

    // Slow Mars movement
    marsGroup.position.y =
        0.8 + Math.sin(time * 0.18) * 0.025;

    // Keep labels attached to planets
    updateLabel(moonGroup, moonLabel);

    updateLabel(marsGroup, marsLabel);

    renderer.render(scene, camera);
}

animate();


// =====================================
// REALISTIC SLOW TWINKLING STARS
// =====================================

// ==========================================
// CINEMATIC DEEP SPACE STARFIELD
// ==========================================

const canvas = document.getElementById("stars");
const ctx = canvas.getContext("2d");

let stars = [];
let dustParticles = [];

let canvasWidth = 0;
let canvasHeight = 0;
let dpr = 1;


// Create different layers of stars
function resizeStars() {

    dpr = Math.min(window.devicePixelRatio || 1, 2);

    canvasWidth = canvas.clientWidth;
    canvasHeight = canvas.clientHeight;

    canvas.width = canvasWidth * dpr;
    canvas.height = canvasHeight * dpr;

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    stars = [];
    dustParticles = [];

    // Distant tiny stars
    for (let i = 0; i < 750; i++) {

        stars.push({

            x: Math.random() * canvasWidth,
            y: Math.random() * canvasHeight,

            radius: Math.random() * 0.55 + 0.15,

            base: Math.random() * 0.3 + 0.25,

            phase: Math.random() * Math.PI * 2,

            // Very slow twinkling
            speed: 0.000035 + Math.random() * 0.00007,

            layer: 1

        });

    }

    // Medium-distance stars
    for (let i = 0; i < 180; i++) {

        stars.push({

            x: Math.random() * canvasWidth,
            y: Math.random() * canvasHeight,

            radius: Math.random() * 0.9 + 0.4,

            base: Math.random() * 0.35 + 0.35,

            phase: Math.random() * Math.PI * 2,

            speed: 0.000025 + Math.random() * 0.00006,

            layer: 2

        });

    }

    // A few bright distant stars
    for (let i = 0; i < 28; i++) {

        stars.push({

            x: Math.random() * canvasWidth,
            y: Math.random() * canvasHeight,

            radius: Math.random() * 1.1 + 0.8,

            base: 0.55,

            phase: Math.random() * Math.PI * 2,

            speed: 0.00002 + Math.random() * 0.000035,

            layer: 3

        });

    }

    // Cosmic dust
    for (let i = 0; i < 100; i++) {

        dustParticles.push({

            x: Math.random() * canvasWidth,
            y: Math.random() * canvasHeight,

            radius: Math.random() * 1.1 + 0.3,

            opacity: Math.random() * 0.12 + 0.025,

            speed: Math.random() * 0.012 + 0.003

        });

    }

}


// Draw a star
function drawStar(star, time) {

    const variation =
        0.5 + 0.5 *
        Math.sin(time * star.speed + star.phase);

    const brightness =
        star.base + variation * 0.22;

    ctx.beginPath();

    ctx.arc(
        star.x,
        star.y,
        star.radius,
        0,
        Math.PI * 2
    );

    ctx.fillStyle =
        `rgba(220,230,255,${brightness})`;

    ctx.fill();

    // Soft glow only for brighter stars
    if (star.layer === 3) {

        ctx.beginPath();

        ctx.arc(
            star.x,
            star.y,
            star.radius * 3,
            0,
            Math.PI * 2
        );

        ctx.fillStyle =
            `rgba(120,170,255,${brightness * 0.08})`;

        ctx.fill();

    }

}


// Draw drifting cosmic dust
function drawDust() {

    dustParticles.forEach(particle => {

        particle.x -= particle.speed * 0.15;

        if (particle.x < 0) {
            particle.x = canvasWidth;
        }

        ctx.beginPath();

        ctx.arc(
            particle.x,
            particle.y,
            particle.radius,
            0,
            Math.PI * 2
        );

        ctx.fillStyle =
            `rgba(155,175,230,${particle.opacity})`;

        ctx.fill();

    });

}


// Main animation
function animateStars(time) {

    ctx.clearRect(
        0,
        0,
        canvasWidth,
        canvasHeight
    );

    // Draw distant stars first
    stars.forEach(star => {

        drawStar(star, time);

    });

    drawDust();

    requestAnimationFrame(animateStars);

}


// Start animation
resizeStars();

requestAnimationFrame(animateStars);


// =====================================
// RESPONSIVE
// =====================================

window.addEventListener("resize", () => {

    const width = container.clientWidth;

    const height = container.clientHeight;

    camera.aspect = width / height;

    camera.updateProjectionMatrix();

    renderer.setSize(width, height);

    resizeStars();

});

</script>

</body>
</html>
""", height=500, scrolling=False)


st.markdown(
    '<h1 style="color: #00BFFF;">PLANETARY ENVIRONMENT AND MINERAL ANALYZER</h1>',
    unsafe_allow_html=True
)

# --------------------------------
# PLANETARY ENVIRONMENT ANALYSIS
# --------------------------------


st.header("🌌 Planetary Environmental Analysis")

environment_data = {

    "Earth": {
        "Temperature": "Varies by location",
        "Atmosphere": "Nitrogen and Oxygen",
        "Water": "Liquid water widely available",
        "Minerals": "Silicates, oxides and many others",
        "Radiation": "Protected partly by atmosphere and magnetic field"
    },

    "Moon": {
        "Temperature": "Approximately -173°C to 127°C",
        "Atmosphere": "Extremely thin exosphere",
        "Water": "Water ice in some permanently shadowed regions",
        "Minerals": "Pyroxene, olivine and plagioclase",
        "Radiation": "High surface radiation exposure"
    },

    "Mars": {
        "Temperature": "Average approximately -63°C",
        "Atmosphere": "Mostly carbon dioxide",
        "Water": "Water ice and evidence of ancient liquid water",
        "Minerals": "Olivine, pyroxene and iron oxides",
        "Radiation": "Higher surface exposure than Earth"
    }
}

selected_planet = st.selectbox(
    "Choose Planet for Environmental Analysis",
    ["Earth", "Moon", "Mars"],
    key="environment_planet"
)

st.subheader(
    f"{selected_planet} Environmental Information"
)

selected_data = environment_data[selected_planet]

for parameter, value in selected_data.items():

    st.write(f"**{parameter}:** {value}")

st.divider()




# EARTH LOCATION COMPARISON


# MINERAL COMPOSITION ANALYZER

st.header("🪨 Mineral Composition Analyzer")

mineral_data = {
    "Earth": ["Quartz", "Feldspar", "Mica", "Olivine"],
    "Moon": ["Pyroxene", "Olivine", "Plagioclase"],
    "Mars": ["Olivine", "Pyroxene", "Iron Oxides"]
}

selected_body = st.selectbox(
    "Select Planet or Moon",
    ["Earth", "Moon", "Mars"],
    key="mineral_planet"
)

st.write("### Common Minerals")

for mineral in mineral_data[selected_body]:
    st.write("🔹", mineral)

st.caption(
    "Note: This is a general educational list, not a measured "
    "mineral analysis of a specific location."
)




# -------------------------------
# PLANETARY REFERENCE DATA
# -------------------------------

planet_data = {

    "Mars": {

        "Jezero Crater": {
            "slope": 5,
            "roughness": 65,
            "thermal": 35,
            "rockiness": 75
        },

        "Gale Crater": {
            "slope": 8,
            "roughness": 70,
            "thermal": 45,
            "rockiness": 80
        },

        "Olympus Mons": {
            "slope": 15,
            "roughness": 85,
            "thermal": 30,
            "rockiness": 90
        },

        "Valles Marineris": {
            "slope": 25,
            "roughness": 95,
            "thermal": 40,
            "rockiness": 85
        },

        "Utopia Planitia": {
            "slope": 4,
            "roughness": 55,
            "thermal": 25,
            "rockiness": 65
        }
    },

    "Moon": {

        "Lunar South Pole": {
            "slope": 6,
            "roughness": 75,
            "thermal": 25,
            "rockiness": 85
        },

        "Lunar North Pole": {
            "slope": 7,
            "roughness": 70,
            "thermal": 30,
            "rockiness": 80
        },

        "Sea of Tranquility": {
            "slope": 3,
            "roughness": 40,
            "thermal": 60,
            "rockiness": 55
        },

        "Oceanus Procellarum": {
            "slope": 5,
            "roughness": 50,
            "thermal": 55,
            "rockiness": 65
        },

        "Tycho Crater": {
            "slope": 18,
            "roughness": 90,
            "thermal": 45,
            "rockiness": 95
        }
    }
}

# -------------------------------
# EARTH LOCATION DATABASE
# -------------------------------

earth_locations = {
    "Atacama Desert, Chile": {
        "slope": 5, "roughness": 60, "thermal": 40,
        "rockiness": 70, "latitude": -24.6, "longitude": -69.25
    },
    "Death Valley, USA": {
        "slope": 8, "roughness": 65, "thermal": 75,
        "rockiness": 55, "latitude": 36.24, "longitude": -116.82
    },
    "Antarctica": {
        "slope": 6, "roughness": 70, "thermal": 20,
        "rockiness": 65, "latitude": -82.86, "longitude": 135
    },
    "Hawaiian Volcanic Region": {
        "slope": 12, "roughness": 85, "thermal": 60,
        "rockiness": 90, "latitude": 19.42, "longitude": -155.29
    },
    "McMurdo Dry Valleys, Antarctica": {
        "slope": 7, "roughness": 75, "thermal": 15,
        "rockiness": 80, "latitude": -77.5, "longitude": 161.5
    },
    "Svalbard, Norway": {
        "slope": 10, "roughness": 70, "thermal": 20,
        "rockiness": 65, "latitude": 78.2, "longitude": 15.6
    },
    "Iceland": {
        "slope": 12, "roughness": 80, "thermal": 35,
        "rockiness": 90, "latitude": 64.9, "longitude": -19.0
    },
    "Mojave Desert, USA": {
        "slope": 6, "roughness": 55, "thermal": 70,
        "rockiness": 60, "latitude": 35.0, "longitude": -116.5
    },
    "Utah Desert, USA": {
        "slope": 9, "roughness": 75, "thermal": 50,
        "rockiness": 85, "latitude": 38.5, "longitude": -110.5
    },
    "Arizona Volcanic Field, USA": {
        "slope": 15, "roughness": 85, "thermal": 45,
        "rockiness": 90, "latitude": 35.4, "longitude": -111.5
    },
    "Namib Desert, Namibia": {
        "slope": 5, "roughness": 65, "thermal": 65,
        "rockiness": 50, "latitude": -24.5, "longitude": 15.5
    },
    "Sahara Desert, Africa": {
        "slope": 4, "roughness": 55, "thermal": 80,
        "rockiness": 60, "latitude": 23.0, "longitude": 13.0
    },
    "Haughton Crater, Canada": {
        "slope": 10, "roughness": 85, "thermal": 25,
        "rockiness": 90, "latitude": 75.37, "longitude": -89.68
    },

    "Rio Tinto, Spain": {
        "slope": 8, "roughness": 65, "thermal": 45,
        "rockiness": 80, "latitude": 37.69, "longitude": -6.56
    },

    "Pilbara Craton, Australia": {
        "slope": 7, "roughness": 75, "thermal": 65,
        "rockiness": 90, "latitude": -21.30, "longitude": 119.70
    },

    "University Valley, Antarctica": {
        "slope": 5, "roughness": 70, "thermal": 15,
        "rockiness": 75, "latitude": -79.88, "longitude": 160.76
    },

    "Yellowstone, USA": {
        "slope": 12, "roughness": 75, "thermal": 60,
        "rockiness": 70, "latitude": 44.60, "longitude": -110.50
    },

    "Moab, Utah, USA": {
        "slope": 10, "roughness": 85, "thermal": 65,
        "rockiness": 90, "latitude": 38.57, "longitude": -109.55
    },

    "Cinder Lake, USA": {
        "slope": 5, "roughness": 80, "thermal": 50,
        "rockiness": 85, "latitude": 35.20, "longitude": -111.30
    },

    "Frasassi Cave, Italy": {
        "slope": 5, "roughness": 55, "thermal": 20,
        "rockiness": 70, "latitude": 43.40, "longitude": 12.96
    },

    "Wadi Rum, Jordan": {
        "slope": 12, "roughness": 85, "thermal": 75,
        "rockiness": 90, "latitude": 29.58, "longitude": 35.42
    },

    "Danakil Depression, Ethiopia": {
        "slope": 5, "roughness": 70, "thermal": 90,
        "rockiness": 75, "latitude": 14.24, "longitude": 40.30
    },

    "Laguna Negra, Chile": {
        "slope": 15, "roughness": 70, "thermal": 25,
        "rockiness": 65, "latitude": -33.65, "longitude": -70.10
    },

    "Ladakh, India": {
        "slope": 15, "roughness": 75, "thermal": 20,
        "rockiness": 80, "latitude": 34.15, "longitude": 77.58
    },

    "Tibetan Plateau": {
        "slope": 12, "roughness": 70, "thermal": 25,
        "rockiness": 75, "latitude": 32.00, "longitude": 88.00
    },

    "Sahara Region, Morocco": {
        "slope": 5, "roughness": 65, "thermal": 80,
        "rockiness": 60, "latitude": 30.00, "longitude": -5.00
    },

    "Cappadocia, Turkey": {
        "slope": 10, "roughness": 85, "thermal": 45,
        "rockiness": 80, "latitude": 38.64, "longitude": 34.83
    },
}
# --------------------------------
# GLOBAL ANALOGUE EXPLORER
# --------------------------------

st.divider()
st.markdown(
    '<h1 style="color: #00BFFF;">GLOBAL ANALOGUE EXPLORER</h1>',
    unsafe_allow_html=True
)

st.header("🌍 Global Analogue Explorer")

st.write(
    "Search and explore Earth locations "
    "that may be useful for Moon and Mars analogue research."
)

# LOCATION FILTERS

continent_data = {
    "Atacama Desert, Chile": "South America",
    "Death Valley, USA": "North America",
    "Antarctica": "Antarctica",
    "Hawaiian Volcanic Region": "North America",
    "McMurdo Dry Valleys, Antarctica": "Antarctica",
    "Svalbard, Norway": "Europe",
    "Iceland": "Europe",
    "Mojave Desert, USA": "North America",
    "Utah Desert, USA": "North America",
    "Arizona Volcanic Field, USA": "North America",
    "Namib Desert, Namibia": "Africa",
    "Sahara Desert, Africa": "Africa",
    "Haughton Crater, Canada": "North America",
    "Rio Tinto, Spain": "Europe",
    "Pilbara Craton, Australia": "Oceania",
    "University Valley, Antarctica": "Antarctica",
    "Yellowstone, USA": "North America",
    "Moab, Utah, USA": "North America",
    "Cinder Lake, USA": "North America",
    "Frasassi Cave, Italy": "Europe",
    "Wadi Rum, Jordan": "Asia",
    "Danakil Depression, Ethiopia": "Africa",
    "Laguna Negra, Chile": "South America",
    "Ladakh, India": "Asia",
    "Tibetan Plateau": "Asia",
    "Sahara Region, Morocco": "Africa",
    "Cappadocia, Turkey": "Asia"
}
# SUGGESTED PLANETARY RESEARCH CATEGORIES

analogue_categories = {

    "Atacama Desert, Chile": "Mars",
    "Death Valley, USA": "Mars",
    "Antarctica": "Both",
    "Hawaiian Volcanic Region": "Both",
    "McMurdo Dry Valleys, Antarctica": "Mars",
    "Svalbard, Norway": "Both",
    "Iceland": "Both",
    "Mojave Desert, USA": "Mars",
    "Utah Desert, USA": "Mars",
    "Arizona Volcanic Field, USA": "Moon",
    "Namib Desert, Namibia": "Mars",
    "Sahara Desert, Africa": "Mars",
    "Haughton Crater, Canada": "Both",
    "Rio Tinto, Spain": "Mars",
    "Pilbara Craton, Australia": "Mars",
    "University Valley, Antarctica": "Mars",
    "Yellowstone, USA": "Both",
    "Moab, Utah, USA": "Mars",
    "Cinder Lake, USA": "Moon",
    "Frasassi Cave, Italy": "Mars",
    "Wadi Rum, Jordan": "Mars",
    "Danakil Depression, Ethiopia": "Mars",
    "Laguna Negra, Chile": "Both",
    "Ladakh, India": "Both",
    "Tibetan Plateau": "Both",
    "Sahara Region, Morocco": "Mars",
    "Cappadocia, Turkey": "Moon"
}

# ==========================================
# ADDITIONAL 20 EARTH ANALOGUE LOCATIONS
# ==========================================

earth_locations.update({

    "Spiti Valley, India": {
        "slope": 12, "roughness": 75, "thermal": 20,
        "rockiness": 85, "latitude": 32.25, "longitude": 78.00
    },

    "Rann of Kutch, India": {
        "slope": 2, "roughness": 35, "thermal": 75,
        "rockiness": 25, "latitude": 23.73, "longitude": 70.50
    },

    "Lonar Crater, India": {
        "slope": 15, "roughness": 80, "thermal": 55,
        "rockiness": 85, "latitude": 19.98, "longitude": 76.51
    },

    "Barren Island, India": {
        "slope": 25, "roughness": 90, "thermal": 65,
        "rockiness": 95, "latitude": 12.28, "longitude": 93.86
    },

    "Salar de Uyuni, Bolivia": {
        "slope": 2, "roughness": 25, "thermal": 35,
        "rockiness": 15, "latitude": -20.13, "longitude": -67.49
    },

    "Lanzarote Volcanic Fields, Spain": {
        "slope": 12, "roughness": 85, "thermal": 55,
        "rockiness": 95, "latitude": 29.04, "longitude": -13.64
    },

    "Mauna Kea, Hawaii": {
        "slope": 18, "roughness": 90, "thermal": 25,
        "rockiness": 90, "latitude": 19.82, "longitude": -155.47
    },

    "Etna Volcano, Italy": {
        "slope": 20, "roughness": 90, "thermal": 45,
        "rockiness": 90, "latitude": 37.75, "longitude": 14.99
    },

    "Afar Depression, Ethiopia": {
        "slope": 5, "roughness": 75, "thermal": 90,
        "rockiness": 70, "latitude": 11.50, "longitude": 41.00
    },

    "Patagonia, Argentina": {
        "slope": 10, "roughness": 70, "thermal": 25,
        "rockiness": 75, "latitude": -49.00, "longitude": -73.00
    },

    "Svalbard Glacier Region, Norway": {
        "slope": 15, "roughness": 80, "thermal": 10,
        "rockiness": 70, "latitude": 78.00, "longitude": 16.00
    },

    "Kalaallit Nunaat Ice Sheet, Greenland": {
        "slope": 8, "roughness": 45, "thermal": 5,
        "rockiness": 20, "latitude": 70.00, "longitude": -40.00
    },

    "Kilauea Volcanic Region, Hawaii": {
        "slope": 10, "roughness": 85, "thermal": 65,
        "rockiness": 95, "latitude": 19.42, "longitude": -155.29
    },

    "Black Rock Desert, USA": {
        "slope": 3, "roughness": 40, "thermal": 60,
        "rockiness": 35, "latitude": 40.80, "longitude": -119.00
    },

    "Ayers Rock Region, Australia": {
        "slope": 8, "roughness": 75, "thermal": 70,
        "rockiness": 90, "latitude": -25.34, "longitude": 131.03
    },

    "Mount Erebus, Antarctica": {
        "slope": 22, "roughness": 90, "thermal": 10,
        "rockiness": 95, "latitude": -77.53, "longitude": 167.17
    },

    "Tenerife Volcanic Region, Spain": {
        "slope": 20, "roughness": 85, "thermal": 45,
        "rockiness": 90, "latitude": 28.27, "longitude": -16.64
    },

    "Qaidam Basin, China": {
        "slope": 4, "roughness": 65, "thermal": 30,
        "rockiness": 65, "latitude": 37.00, "longitude": 95.00
    },

    "Dallol Geothermal Region, Ethiopia": {
        "slope": 5, "roughness": 80, "thermal": 95,
        "rockiness": 65, "latitude": 14.24, "longitude": 40.30
    },

    "Namcha Barwa Region, Tibet": {
        "slope": 30, "roughness": 90, "thermal": 15,
        "rockiness": 85, "latitude": 29.63, "longitude": 95.06
    }
})


# ==========================================
# CONTINENT INFORMATION
# ==========================================

continent_data.update({

    "Spiti Valley, India": "Asia",
    "Rann of Kutch, India": "Asia",
    "Lonar Crater, India": "Asia",
    "Barren Island, India": "Asia",
    "Salar de Uyuni, Bolivia": "South America",
    "Lanzarote Volcanic Fields, Spain": "Europe",
    "Mauna Kea, Hawaii": "North America",
    "Etna Volcano, Italy": "Europe",
    "Afar Depression, Ethiopia": "Africa",
    "Patagonia, Argentina": "South America",
    "Svalbard Glacier Region, Norway": "Europe",
    "Kalaallit Nunaat Ice Sheet, Greenland": "North America",
    "Kilauea Volcanic Region, Hawaii": "North America",
    "Black Rock Desert, USA": "North America",
    "Ayers Rock Region, Australia": "Oceania",
    "Mount Erebus, Antarctica": "Antarctica",
    "Tenerife Volcanic Region, Spain": "Europe",
    "Qaidam Basin, China": "Asia",
    "Dallol Geothermal Region, Ethiopia": "Africa",
    "Namcha Barwa Region, Tibet": "Asia"
})


# ==========================================
# PLANETARY ANALOGUE CATEGORIES
# ==========================================

analogue_categories.update({

    "Spiti Valley, India": "Mars",
    "Rann of Kutch, India": "Both",
    "Lonar Crater, India": "Both",
    "Barren Island, India": "Moon",
    "Salar de Uyuni, Bolivia": "Mars",
    "Lanzarote Volcanic Fields, Spain": "Moon",
    "Mauna Kea, Hawaii": "Both",
    "Etna Volcano, Italy": "Moon",
    "Afar Depression, Ethiopia": "Mars",
    "Patagonia, Argentina": "Mars",
    "Svalbard Glacier Region, Norway": "Both",
    "Kalaallit Nunaat Ice Sheet, Greenland": "Moon",
    "Kilauea Volcanic Region, Hawaii": "Moon",
    "Black Rock Desert, USA": "Mars",
    "Ayers Rock Region, Australia": "Mars",
    "Mount Erebus, Antarctica": "Both",
    "Tenerife Volcanic Region, Spain": "Moon",
    "Qaidam Basin, China": "Mars",
    "Dallol Geothermal Region, Ethiopia": "Mars",
    "Namcha Barwa Region, Tibet": "Mars"
})

col1, col2 = st.columns(2)

with col1:
    selected_continent = st.selectbox(
        "Select Continent",
        ["All"] + sorted(set(continent_data.values())),
        key="global_continent"
    )

with col2:
    search_location = st.text_input(
        "Search Location",
        placeholder="Example: Ladakh",
        key="global_search"
    )
    selected_analogue = st.selectbox(
    "Select Research Category",
    ["All", "Mars", "Moon"],
    key="analogue_filter"
)

# FILTER LOCATIONS

filtered_locations = []

for name, data in earth_locations.items():
    if selected_analogue != "All":
        category = analogue_categories.get(name, "Both")

        if category not in [selected_analogue, "Both"]:
            continue

    if selected_continent != "All":
        if continent_data.get(name) != selected_continent:
            continue

    if search_location.lower() not in name.lower():
        continue

    filtered_locations.append((name, data))

st.write(
    f"### {len(filtered_locations)} locations found"
)

# DISPLAY FILTERED MAP

global_map = folium.Map(
    location=[20, 0],
    zoom_start=2
)

for name, data in filtered_locations:

    popup_text = f"""
    <b>{name}</b><br>
    Latitude: {data['latitude']}<br>
    Longitude: {data['longitude']}
    """

    folium.Marker(
        location=[
            data["latitude"],
            data["longitude"]
        ],
        popup=folium.Popup(popup_text, max_width=300),
        tooltip=name,
        icon=folium.Icon(color="blue")
    ).add_to(global_map)

st_folium(
    global_map,
    width=1100,
    height=600,
    key="filtered_global_map"
)

st.caption(
    "Map markers show approximate candidate locations. "
    "Environmental values are illustrative prototype data."
)
# EARTH LOCATION COMPARISON

st.header("🌍 Earth Location Comparison")

location_names = list(earth_locations.keys())

selected_locations = st.multiselect(
    "Choose Earth locations to compare",
    location_names,
    default=location_names[:2],
    key="location_comparison"
)

if selected_locations:

    comparison_data = []

    for name in selected_locations:

        data = earth_locations[name]

        comparison_data.append({
            "Location": name,
            "Slope": data["slope"],
            "Roughness": data["roughness"],
            "Thermal Index": data["thermal"],
            "Rockiness": data["rockiness"]
        })

    # COMPARISON TABLE

    st.subheader("📋 Comparison Results")

    st.dataframe(
        comparison_data,
        width="stretch",
        hide_index=True
    )

    # COMPARISON CHART

    st.subheader("📊 Environmental Comparison Chart")

    chart_data = pd.DataFrame(comparison_data)

    chart_data = chart_data.set_index("Location")[
        ["Slope", "Roughness", "Thermal Index", "Rockiness"]
    ]

    st.bar_chart(chart_data)

    # DOWNLOAD REPORT

    csv_data = pd.DataFrame(comparison_data).to_csv(index=False)

    st.download_button(
        label="📥 Download Comparison Report",
        data=csv_data,
        file_name="earth_location_comparison.csv",
        mime="text/csv"
    )

else:

    st.info("Select at least one location to compare.")

# -------------------------------
# SIMILARITY CALCULATION
# -------------------------------

# SCIENTIFIC COMPARISON WEIGHTS

weights = {
    "slope": 0.30,
    "roughness": 0.25,
    "thermal": 0.25,
    "rockiness": 0.20
}

# Maximum difference used for normalization

parameter_ranges = {
    "slope": 45,
    "roughness": 100,
    "thermal": 100,
    "rockiness": 100
}


# ADVANCED SIMILARITY ALGORITHM

def calculate_similarity(reference, earth):

    total_score = 0

    parameter_scores = {}

    for parameter, weight in weights.items():

        difference = abs(
            reference[parameter] -
            earth[parameter]
        )

        max_difference = parameter_ranges[parameter]

        similarity = (
            1 - difference / max_difference
        ) * 100

        similarity = max(
            0,
            min(100, similarity)
        )

        parameter_scores[parameter] = round(
            similarity, 2
        )

        total_score += similarity * weight

    return round(total_score, 2), parameter_scores


# -------------------------------
# USER SELECTION
# -------------------------------
st.divider()
st.markdown(
    '<h1 style="color: #00BFFF;">EARTH ANALOGUE FINDER</h1>',
    unsafe_allow_html=True
)

st.header("🌍 Earth to Moon and Mars Terrain Comparison")

st.write(
    "Select a planetary region and discover "
    "Earth locations with similar terrain characteristics."
)
st.header("Select Planetary Region")

col1, col2 = st.columns(2)

with col1:

    planet = st.selectbox(
        "Select Planet",
        ["Mars", "Moon"]
    )

with col2:

    region = st.selectbox(
        "Select Region",
        list(planet_data[planet].keys())
    )

reference = planet_data[planet][region]
# PLANETARY REGION INFORMATION

region_info = {

    "Jezero Crater":
        "Mars region known for evidence of an ancient lake "
        "and a preserved river delta.",

    "Gale Crater":
        "Mars impact crater explored by NASA's Curiosity rover.",

    "Olympus Mons":
        "A giant shield volcano on Mars.",

    "Valles Marineris":
        "A vast canyon system on Mars.",

    "Utopia Planitia":
        "A large plain in the northern hemisphere of Mars.",

    "Lunar South Pole":
        "Lunar polar region containing permanently shadowed "
        "areas of scientific interest.",

    "Lunar North Pole":
        "A lunar polar region with permanently shadowed terrain.",

    "Sea of Tranquility":
        "A lunar basaltic plain and landing region of Apollo 11.",

    "Oceanus Procellarum":
        "A large basaltic plain on the Moon.",

    "Tycho Crater":
        "A prominent impact crater on the Moon."
}


st.subheader("🪐 Planetary Region Information")

st.info(region_info[region])

st.subheader("Scientific Parameter Reference")

parameter_df = pd.DataFrame(
    list(reference.items()),
    columns=["Parameter", "Prototype Value"]
)

st.dataframe(
    parameter_df,
    width="stretch",
    hide_index=True
)

st.bar_chart(
    parameter_df.set_index("Parameter")
)
st.divider()
st.subheader("Click Here")
# -------------------------------
# FIND EARTH ANALOGS
# -------------------------------

# --------------------------------
# STORE COMPARISON RESULTS
# --------------------------------

if "results" not in st.session_state:
    st.session_state.results = None

# --------------------------------
# FIND EARTH ANALOGS
# --------------------------------

if st.button("🚀 FIND EARTH ANALOGS"):

    results = []

    for location, data in earth_locations.items():

        similarity, details = calculate_similarity(
            reference,
            data
        )

        results.append({

            "Earth Location": location,

            "Similarity Score (%)": similarity,

            "Slope Match (%)": details["slope"],

            "Roughness Match (%)": details["roughness"],

            "Thermal Match (%)": details["thermal"],

            "Rockiness Match (%)": details["rockiness"]

        })

        

    results = sorted(
        results,
        key=lambda x: x["Similarity Score (%)"],
        reverse=True
    )

    st.session_state.results = results


# --------------------------------
# DISPLAY STORED RESULTS
# --------------------------------

if st.session_state.results is not None:

    results = st.session_state.results

    st.header("📊 Comparison Results")

    df = pd.DataFrame(results)

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )

    # BEST LOCATION

    best = results[0]

    st.success(
        f"Best illustrative match: {best['Earth Location']}"
    )

    st.metric(
        "Illustrative Similarity",
        f"{best['Similarity Score (%)']}%"
    )

    # CHART

    st.subheader("📈 Similarity Chart")

    chart = df.set_index("Earth Location")

    st.bar_chart(chart)
# PARAMETER-WISE COMPARISON

    st.subheader("Scientific Parameter Comparison")

    selected_location = st.selectbox(
        "Select Earth Location for Detailed Analysis",
        [item["Earth Location"] for item in results],
        key="detailed_location"
    )

    selected_result = next(
        item for item in results
        if item["Earth Location"] == selected_location
    )

    comparison_data = pd.DataFrame({

        "Parameter": [
            "Slope",
            "Roughness",
            "Thermal",
            "Rockiness"
        ],

        "Similarity (%)": [
            selected_result["Slope Match (%)"],
            selected_result["Roughness Match (%)"],
            selected_result["Thermal Match (%)"],
            selected_result["Rockiness Match (%)"]
        ]
    })

    st.bar_chart(
        comparison_data.set_index("Parameter")
    )

    st.dataframe(
        comparison_data,
        width="stretch",
        hide_index=True
    )
    # MAP

    st.header("🌍 Interactive Earth Map")

    earth_map = folium.Map(
        location=[10, 0],
        zoom_start=2
    )

    for result in results:

        location = result["Earth Location"]

        data = earth_locations[location]

        score = result["Similarity Score (%)"]

        color = (
            "green"
            if location == best["Earth Location"]
            else "blue"
        )

        popup = f"""
        <b>{location}</b><br>
        Similarity: {score}%<br>
        Latitude: {data['latitude']}<br>
        Longitude: {data['longitude']}
        """

        folium.Marker(
            location=[
                data["latitude"],
                data["longitude"]
            ],
            popup=popup,
            tooltip=location,
            icon=folium.Icon(color=color)
        ).add_to(earth_map)

    st_folium(
        earth_map,
        width=1100,
        height=550,
        key="earth_analog_map"
    )

    st.caption(
        "Green marker = highest illustrative score. "
        "Blue markers = other candidate locations."
    )

    st.info(
        "Prototype results use illustrative data, "
        "not verified scientific measurements."
    )
    # --------------------------------
# SIMILARITY METHODOLOGY
# --------------------------------

st.divider()

st.header("🧪 Similarity Score Methodology")

st.write(
    "SPACE ANALOG FINDER compares selected environmental "
    "parameters between a planetary region and Earth locations."
)

st.subheader("Comparison Parameters")

methodology_data = {
    "Parameter": [
        "Slope",
        "Roughness",
        "Thermal Index",
        "Rockiness"
    ],
    "Weight": [
        "30%",
        "25%",
        "25%",
        "20%"
    ],
    "Purpose": [
        "Compares terrain steepness.",
        "Compares surface irregularity.",
        "Compares the prototype thermal index.",
        "Compares rocky surface characteristics."
    ]
}

methodology_df = pd.DataFrame(methodology_data)

st.dataframe(
    methodology_df,
    width="stretch",
    hide_index=True
)

st.subheader("How the Score Works")

st.latex(
    r"Similarity = "
    r"\left(1 - \frac{|A-B|}{R}\right)\times 100"
)

st.write(
    "A and B represent the two values being compared. "
    "R is the maximum difference used for normalization."
)

st.info(
    "The overall score is a weighted combination of the "
    "four parameter similarity scores."
)

st.warning(
    "Current numerical inputs are illustrative prototype "
    "values, not verified scientific measurements. "
    "The scores demonstrate the algorithm and should not "
    "be interpreted as validated planetary analogue rankings."
)
# --------------------------------
# INDIVIDUAL LOCATION PROFILES
# --------------------------------

st.divider()
st.markdown(
    '<h1 style="color: #00BFFF;">RESEARCH</h1>',
    unsafe_allow_html=True
)

st.header("📍 Earth Analogue Location Profiles")

st.write(
    "Explore detailed information about each location "
    "in the global analogue database."
)

# SELECT LOCATION

profile_location = st.selectbox(
    "Choose an Earth Location",
    list(earth_locations.keys()),
    key="location_profile_selector"
)

# GET LOCATION DATA

profile_data = earth_locations[profile_location]

# LOCATION INFORMATION

st.subheader(f"🌍 {profile_location}")
# LOCATION PHOTOGRAPHS AND RESEARCH


# --------------------------------
# LOCATION RESEARCH AND PHOTOGRAPHS
# --------------------------------

import requests
from urllib.parse import quote

# RESEARCH INFORMATION FOR LOCATIONS

location_research = {

    "Atacama Desert, Chile": {
        "description": "One of Earth's driest regions. Its extremely dry environment makes it useful for studying conditions relevant to Mars exploration.",
        "planet": "Mars",
        "source": "NASA Planetary Analog Explorer",
        "url": "https://science.nasa.gov/solar-system/analog-explorer/"
    },

    "Iceland": {
        "description": "Iceland has volcanic landscapes, glaciers and ice-covered environments that can help researchers study geological processes relevant to the Moon and Mars.",
        "planet": "Moon and Mars",
        "source": "NASA Planetary Analog Explorer",
        "url": "https://science.nasa.gov/solar-system/analog-explorer/"
    },

    "Death Valley, USA": {
        "description": "This dry and rugged desert environment is useful for studying extreme conditions and testing exploration technologies.",
        "planet": "Mars",
        "source": "NASA Planetary Analogs",
        "url": "https://science.nasa.gov/solar-system/planetary-analogs/"
    },

    "Hawaiian Volcanic Region": {
        "description": "Volcanic landscapes and lava fields provide useful comparisons for understanding volcanic features on the Moon and Mars.",
        "planet": "Moon and Mars",
        "source": "NASA Planetary Analog Explorer",
        "url": "https://science.nasa.gov/solar-system/analog-explorer/"
    },

    "Moab, Utah, USA": {
        "description": "The desert landscapes and rock formations of Utah provide useful comparisons for studying Martian geology and terrain.",
        "planet": "Mars",
        "source": "NASA Planetary Analog Explorer",
        "url": "https://science.nasa.gov/solar-system/analog-explorer/"
    }
}


# --------------------------------
# SCIENTIFIC RESEARCH SECTION
# --------------------------------

st.divider()

st.header("🔬 Scientific Research Information")

research = location_research.get(profile_location)

if research:

    st.success("Research information available")

    st.write("**Selected Location:**", profile_location)

    st.write("**Planetary Analogue:**", research["planet"])

    st.write("**Scientific Description:**")
    st.write(research["description"])

    st.write("**Research Reference:**", research["source"])

    st.link_button(
        "🌐 Open Research Reference",
        research["url"]
    )

else:

    # General information for other selected locations

    selected_category = analogue_categories.get(
        profile_location,
        "Earth environment"
    )

    st.info("General analogue information")

    st.write("**Selected Location:**", profile_location)

    st.write("**Environment Category:**", selected_category)

    st.write(
        "**Scientific Relevance:**",
        f"{profile_location} can be examined as an Earth environment "
        "for comparing terrain, geology, climate or surface conditions "
        "with possible Moon and Mars exploration sites."
    )

    st.write(
        "**Research Note:** This is a preliminary project-level "
        "comparison, not confirmation of a specific NASA research study."
    )

    st.link_button(
        "🌐 Explore NASA Planetary Analogs",
        "https://science.nasa.gov/solar-system/planetary-analogs/"
    )


# --------------------------------
# LOCATION PHOTOGRAPH GALLERY
# --------------------------------

st.divider()

st.header("📸 Location Photograph Gallery")

st.write(
    f"Explore photographs and visual references for {profile_location}."
)

st.caption(
    "Photographs are searched from Wikimedia Commons."
)

# Search Wikimedia Commons for photographs

try:

    image_response = requests.get(
        "https://commons.wikimedia.org/w/api.php",

        params={
            "action": "query",
            "generator": "search",
            "gsrsearch": f"{profile_location} landscape",
            "gsrnamespace": 6,
            "gsrlimit": 6,
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": 1000,
            "format": "json"
        },

        headers={
            "User-Agent": "EarthAnalogueFinder/1.0"
        },

        timeout=15
    )

    image_response.raise_for_status()

    image_data = image_response.json()

    pages = image_data.get(
        "query", {}
    ).get(
        "pages", {}
    )

    photo_list = []

    for page in pages.values():

        image_info = page.get(
            "imageinfo", []
        )

        if image_info:

            image_url = image_info[0].get(
                "thumburl",
                image_info[0].get("url")
            )

            image_title = page.get(
                "title",
                "Location photograph"
            )

            if image_url:
                photo_list.append(
                    (image_url, image_title)
                )

    if photo_list:

        st.success(
            f"{len(photo_list)} photograph results found."
        )

        photo_columns = st.columns(3)

        for index, photo in enumerate(photo_list):

            image_url, image_title = photo

            with photo_columns[index % 3]:

                st.image(
                    image_url,
                    caption=image_title.replace("File:", ""),
                    use_container_width=True
                )

    else:

        st.warning(
            "No photographs were returned for this location."
        )

        search_url = (
            "https://commons.wikimedia.org/wiki/Special:MediaSearch"
            "?type=image&search="
            + quote(profile_location)
        )

        st.link_button(
            "View Location Photographs",
            search_url
        )

except Exception as error:

    st.warning(
        "Photographs could not be loaded. "
        "Please check your internet connection."
    )

    search_url = (
        "https://commons.wikimedia.org/wiki/Special:MediaSearch"
        "?type=image&search="
        + quote(profile_location)
    )

    st.link_button(
        "Open Photograph Search",
        search_url
    )

st.caption(
    "Note: These images are visual references. "
    "Check their descriptions and licences before using them "
    "as scientific evidence."
)

# END OF RESEARCH AND PHOTOGRAPH SECTION

continent = continent_data.get(
    profile_location,
    "Not classified"
)

category = analogue_categories.get(
    profile_location,
    "Not classified"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Continent", continent)

with col2:
    st.metric("Research Category", category)

with col3:
    st.metric(
        "Coordinates",
        f"{profile_data['latitude']}, {profile_data['longitude']}"
    )

# ENVIRONMENTAL PARAMETERS

st.subheader("Environmental Parameters")

profile_df = pd.DataFrame({
    "Parameter": [
        "Slope",
        "Roughness",
        "Thermal Index",
        "Rockiness"
    ],
    "Prototype Value": [
        profile_data["slope"],
        profile_data["roughness"],
        profile_data["thermal"],
        profile_data["rockiness"]
    ]
})

st.dataframe(
    profile_df,
    width="stretch",
    hide_index=True
)

# LOCATION MAP

st.subheader("Location on Earth")

profile_map = folium.Map(
    location=[
        profile_data["latitude"],
        profile_data["longitude"]
    ],
    zoom_start=6
)

folium.Marker(
    location=[
        profile_data["latitude"],
        profile_data["longitude"]
    ],
    popup=profile_location,
    tooltip=profile_location
).add_to(profile_map)

st_folium(
    profile_map,
    width=900,
    height=450,
    key="individual_location_profile_map"
)

st.caption(
    "Environmental parameter values are illustrative "
    "prototype inputs, not verified scientific measurements."
)
# --------------------------------
# PLANETARY MISSION SUITABILITY ANALYZER
# --------------------------------

st.divider()
st.markdown(
    '<h1 style="color: #00BFFF;">PLANETARY MISSION CONTROL</h1>',
    unsafe_allow_html=True
)

st.header("🚀 Planetary Mission Suitability Analyzer")

st.write(
    "Evaluate Earth locations for simulated planetary "
    "exploration missions."
)

# SELECT LOCATION

mission_location = st.selectbox(
    "Select Earth Mission Location",
    list(earth_locations.keys()),
    key="mission_location"
)

mission_data = earth_locations[mission_location]

# MISSION TYPE

mission_type = st.selectbox(
    "Select Mission Type",
    [
        "Mars Surface Exploration",
        "Lunar Surface Exploration",
        "Robotic Rover Testing",
        "Astronaut Training"
    ],
    key="mission_type"
)

# SUITABILITY CALCULATION

terrain_score = (
    mission_data["roughness"] * 0.35
    + mission_data["rockiness"] * 0.35
    + (100 - mission_data["slope"]) * 0.30
)

temperature_score = 100 - abs(
    mission_data["thermal"] - 50
)

accessibility_score = (
    100 - mission_data["slope"]
)

research_score = (
    90 if analogue_categories.get(
        mission_location
    ) in ["Mars", "Moon", "Both"]
    else 50
)

overall_score = (
    terrain_score * 0.35
    + temperature_score * 0.20
    + accessibility_score * 0.20
    + research_score * 0.25
)

overall_score = round(overall_score, 2)

# DISPLAY RESULTS

st.subheader("📊 Mission Suitability Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Overall Suitability",
        f"{overall_score}%"
    )

with col2:
    st.metric(
        "Terrain Suitability",
        f"{terrain_score:.1f}%"
    )

with col3:
    st.metric(
        "Temperature Suitability",
        f"{temperature_score:.1f}%"
    )

# ADDITIONAL PARAMETERS

st.subheader("Mission Evaluation Parameters")

mission_results = pd.DataFrame({
    "Parameter": [
        "Terrain Suitability",
        "Temperature Suitability",
        "Accessibility",
        "Research Relevance"
    ],
    "Score (%)": [
        terrain_score,
        temperature_score,
        accessibility_score,
        research_score
    ]
})

st.bar_chart(
    mission_results.set_index("Parameter")
)

st.dataframe(
    mission_results,
    width="stretch",
    hide_index=True
)

# MISSION RATING

st.subheader("🏆 Mission Assessment")

if overall_score >= 80:

    st.success(
        "Excellent illustrative mission suitability."
    )

elif overall_score >= 60:

    st.info(
        "Good illustrative mission suitability."
    )

elif overall_score >= 40:

    st.warning(
        "Moderate illustrative mission suitability."
    )

else:

    st.error(
        "Low illustrative mission suitability."
    )

st.caption(
    "These scores are experimental prototype calculations. "
    "They are not validated engineering assessments or "
    "real mission safety recommendations."
)
# ==========================================
# PHASE 21: PLANETARY MISSION DASHBOARD
# ==========================================
st.header("🪐 Planetary Mission Dashboard")
st.write(
    "Configure a sample planetary mission and explore how different "
    "Earth analogue locations could support mission planning."
)
# Mission configuration
col1, col2 = st.columns(2)
with col1:
    target_planet = st.selectbox(
        "Select Target Planet",
        ["Mars", "Moon"],
        key="dashboard_target"
    )
with col2:
    mission_objective = st.selectbox(
        "Select Mission Objective",
        [
            "Rover Exploration",
            "Astronaut Training",
            "Landing Site Evaluation",
            "Terrain Navigation Testing"
        ],
        key="dashboard_objective"
    )
# Filter locations by planetary category
suitable_locations = []
for location, category in analogue_categories.items():
    if target_planet == "Mars" and category in ["Mars", "Both"]:
        suitable_locations.append(location)
    elif target_planet == "Moon" and category in ["Moon", "Both"]:
        suitable_locations.append(location)
if suitable_locations:
    selected_location = st.selectbox(
        "Choose Earth Analogue Location",
        suitable_locations,
        key="dashboard_location"
    )
    selected_data = earth_locations[selected_location]
    st.subheader("Mission Environment Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Slope", f"{selected_data['slope']}/100")
    col2.metric("Roughness", f"{selected_data['roughness']}/100")
    col3.metric("Thermal Index", f"{selected_data['thermal']}/100")
    col4.metric("Rockiness", f"{selected_data['rockiness']}/100")
    # Illustrative mission indicators
    terrain_readiness = (
        selected_data["roughness"] * 0.35
        + selected_data["rockiness"] * 0.35
        + (100 - selected_data["slope"]) * 0.30
    )
    navigation_readiness = 100 - selected_data["slope"]
    environmental_readiness = (
        100 - abs(selected_data["thermal"] - 50)
    )
    mission_readiness = (
        terrain_readiness * 0.40
        + navigation_readiness * 0.30
        + environmental_readiness * 0.30
    )
    st.subheader("Mission Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Terrain Indicator",
        f"{terrain_readiness:.1f}%"
    )
    col2.metric(
        "Navigation Indicator",
        f"{navigation_readiness:.1f}%"
    )
    col3.metric(
        "Environmental Indicator",
        f"{environmental_readiness:.1f}%"
    )
    st.progress(
        max(0, min(100, int(mission_readiness))),
        text=f"Illustrative Mission Index: {mission_readiness:.1f}%"
    )
    # Comparison chart
    chart_data = pd.DataFrame({
        "Indicator": [
            "Terrain",
            "Navigation",
            "Environment"
        ],
        "Score": [
            terrain_readiness,
            navigation_readiness,
            environmental_readiness
        ]
    })
    st.subheader("Mission Indicator Comparison")
    st.bar_chart(
        chart_data.set_index("Indicator")
    )
    # Mission summary
    st.subheader("Mission Summary")
    st.write(f"**Target:** {target_planet}")
    st.write(f"**Mission Objective:** {mission_objective}")
    st.write(f"**Selected Analogue:** {selected_location}")
    if mission_readiness >= 75:
        st.success(
            "This location has a high illustrative mission index."
        )
    elif mission_readiness >= 50:
        st.warning(
            "This location has a moderate illustrative mission index."
        )
    else:
        st.error(
            "This location has a low illustrative mission index."
        )
    st.caption(
        "Note: These scores are prototype indicators based on the app's "
        "existing location parameters. They are not validated scientific, "
        "engineering, landing-safety, or mission-selection assessments."
    )
else:
    st.warning("No analogue locations are available for this target.")
    
# ==========================================
# PHASE 22: AUTOMATIC BEST ANALOGUE FINDER
# ==========================================

st.divider()
st.markdown(
    '<h1 style="color: #00BFFF;">INSTANT EARTH ANALOGUE</h1>',
    unsafe_allow_html=True
)

st.header("🤖 Automatic Best Earth Analogue Finder")

st.write(
    "Select your target planet and planetary region. "
    "The system will automatically identify the best "
    "matching Earth analogue."
)

# Independent user inputs
col1, col2 = st.columns(2)

with col1:
    auto_planet = st.selectbox(
        "Select Target Planet",
        ["Mars", "Moon"],
        key="auto_planet_selection"
    )

with col2:
    auto_region = st.selectbox(
        "Select Planetary Region",
        list(planet_data[auto_planet].keys()),
        key="auto_region_selection"
    )

# Get reference data from the selected region
auto_reference = planet_data[auto_planet][auto_region]

st.info(
    f"Target: {auto_planet} | Region: {auto_region}"
)

# Filter suitable Earth locations
candidate_locations = []

for location, category in analogue_categories.items():

    if auto_planet == "Mars" and category in ["Mars", "Both"]:
        candidate_locations.append(location)

    elif auto_planet == "Moon" and category in ["Moon", "Both"]:
        candidate_locations.append(location)

# Calculate similarity
automatic_results = []

for location in candidate_locations:

    earth_data = earth_locations[location]

    score, details = calculate_similarity(
        auto_reference,
        earth_data
    )

    automatic_results.append({
        "Earth Location": location,
        "Similarity Score (%)": score,
        "Slope Match (%)": details["slope"],
        "Roughness Match (%)": details["roughness"],
        "Thermal Match (%)": details["thermal"],
        "Rockiness Match (%)": details["rockiness"]
    })

# Rank results
automatic_results = sorted(
    automatic_results,
    key=lambda x: x["Similarity Score (%)"],
    reverse=True
)

# Display recommendation
if automatic_results:

    best_match = automatic_results[0]

    st.success("🏆 BEST EARTH ANALOGUE IDENTIFIED")

    st.title(f"🌍 {best_match['Earth Location']}")

    st.metric(
        "Overall Similarity",
        f"{best_match['Similarity Score (%)']}%"
    )

    st.write(
        f"Best matching location for {auto_region}, "
        f"{auto_planet}."
    )

    st.subheader("Environmental Parameter Matching")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Slope", f"{best_match['Slope Match (%)']}%")
    c2.metric("Roughness", f"{best_match['Roughness Match (%)']}%")
    c3.metric("Thermal", f"{best_match['Thermal Match (%)']}%")
    c4.metric("Rockiness", f"{best_match['Rockiness Match (%)']}%")

    st.subheader("📊 All Analogue Rankings")

    ranking_df = pd.DataFrame(automatic_results)

    ranking_df.insert(
        0,
        "Rank",
        range(1, len(ranking_df) + 1)
    )

    st.dataframe(
        ranking_df,
        width="stretch",
        hide_index=True
    )

    st.subheader("📈 Similarity Chart")

    chart_df = ranking_df[
        ["Earth Location", "Similarity Score (%)"]
    ].set_index("Earth Location")

    st.bar_chart(chart_df)

    st.download_button(
        "📥 Download Analysis Report",
        data=ranking_df.to_csv(index=False),
        file_name="automatic_analogue_report.csv",
        mime="text/csv"
    )

else:
    st.warning("No suitable analogue locations found.")

st.caption(
    "Prototype recommendation based on illustrative data "
    "and the existing similarity algorithm. Not a validated "
    "scientific or mission-safety assessment."
)