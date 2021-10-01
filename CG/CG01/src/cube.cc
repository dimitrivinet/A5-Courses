#include <cstdio>
#include <glad/glad.h>
#include <GLFW/glfw3.h>

#define STB_IMAGE_IMPLEMENTATION
#include <stb/stb_image.h>

#include <glm/glm.hpp>
#include <glm/gtx/transform.hpp>

#include <callbacks.hh>

#define WIDTH 640
#define HEIGHT 480

#define ARRAY_SIZE(array) sizeof(array) / sizeof(array[0])

const char *vertex_shader =
    "#version 400\n"
    "layout(location = 0) in vec3 vp;"
    "uniform mat4 MVP;"
    "void main() {"
    "  gl_Position = MVP * vec4(vp, 1.0);"
    "}";

const char *fragment_shader =
    "#version 400\n"
    "out vec4 frag_colour;"
    "void main() {"
    "  frag_colour = vec4(1.0);"
    "}";

float vertices[]{
    // x, y, z

    // front
    -0.5f, -0.5f, 0.0f, // bottom left, 0
    -0.5f, 0.5f, 0.0f,  // top left, 1
    0.5f, 0.5f, 0.0f,   // top right, 2
    0.5f, -0.5f, 0.0f,  // bottom right, 3

    // back
    -0.5f, -0.5f, -1.0f, // bottom left, 4
    -0.5f, 0.5f, -1.0f,  // top left, 5
    0.5f, 0.5f, -1.0f,   // top right, 6
    0.5f, -0.5f, -1.0f   // bottom right, 7
};

unsigned int indices[]{
    0,
    1,
    2, // front
    0,
    2,
    3,

    0,
    1,
    5, // left
    0,
    5,
    4,

    4,
    5,
    6, // back
    4,
    6,
    7,

    7,
    3,
    2, // right
    7,
    2,
    6,

    2,
    1,
    5, // top
    2,
    5,
    6,

    3,
    0,
    4, // bottom
    3,
    4,
    7,
};

int main()
{
    // Init GLFW
    glfwInit();
    // Set all the required options for GLFW
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    glfwWindowHint(GLFW_RESIZABLE, GL_FALSE);

    // Create a GLFWwindow object that we can use for GLFW's functions
    printf("Creating window\n");
    GLFWwindow *window = glfwCreateWindow(WIDTH, HEIGHT, "CG01", NULL, NULL);
    if (!window)
    {
        printf("Failed creating window.");
        glfwTerminate();
        return EXIT_FAILURE;
    }
    glfwMakeContextCurrent(window);

    // Set the required callback functions
    glfwSetKeyCallback(window, callbacks::keyCallback);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
    {
        printf("Failed to initialize OpenGL context\n");
        return -1;
    }

    // Define the viewport dimensions
    glViewport(0, 0, WIDTH, HEIGHT);

    GLuint vbo, vao, ebo;
    glGenBuffers(1, &vbo);
    glGenVertexArrays(1, &vao);
    glGenBuffers(1, &ebo);

    // vbo stuff
    glBindBuffer(GL_ARRAY_BUFFER, vbo);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

    // vao stuff
    glBindVertexArray(vao);
    glBindBuffer(GL_ARRAY_BUFFER, vbo);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), NULL);
    glEnableVertexAttribArray(0);

    // ebo stuff
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

    // unbind vao
    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glBindVertexArray(0);

    GLuint vs{glCreateShader(GL_VERTEX_SHADER)};
    glShaderSource(vs, 1, &vertex_shader, NULL);
    glCompileShader(vs);

    GLuint fs{glCreateShader(GL_FRAGMENT_SHADER)};
    glShaderSource(fs, 1, &fragment_shader, NULL);
    glCompileShader(fs);

    GLuint shader_program{glCreateProgram()};
    glAttachShader(shader_program, fs);
    glAttachShader(shader_program, vs);
    glLinkProgram(shader_program);

    glDeleteShader(fs);
    glDeleteShader(vs);

    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);

    glm::mat4 Projection = glm::perspective(glm::radians(45.0f), (float)WIDTH / (float)HEIGHT, 0.1f, 100.0f);

    // Or, for an ortho camera :
    //glm::mat4 Projection = glm::ortho(-10.0f,10.0f,-10.0f,10.0f,0.0f,100.0f); // In world coordinates

    // Camera matrix
    glm::mat4 View = glm::lookAt(
        glm::vec3(4, 3, 3), // Camera is at (4,3,3), in World Space
        glm::vec3(0, 0, 0), // and looks at the origin
        glm::vec3(0, 1, 0)  // Head is up (set to 0,-1,0 to look upside-down)
    );

    // Model matrix : an identity matrix (model will be at the origin)
    glm::mat4 Model = glm::mat4(1.0f);
    // Our ModelViewProjection : multiplication of our 3 matrices
    glm::mat4 mvp = Projection * View * Model; // Remember, matrix multiplication is the other way around

    // Get a handle for our "MVP" uniform
    // Only during the initialisation
    GLuint MatrixID = glGetUniformLocation(shader_program, "MVP");

    while (!glfwWindowShouldClose(window))
    {
        // update other events like input handling
        glfwPollEvents();

        // enable depth test
        glEnable(GL_DEPTH_TEST);
        glDepthFunc(GL_LESS);

        // wipe the drawing surface clear
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        // Send our transformation to the currently bound shader, in the "MVP" uniform
        // This is done in the main loop since each model will have a different MVP matrix (At least for the M part)
        glUniformMatrix4fv(MatrixID, 1, GL_FALSE, &mvp[0][0]);

        glUseProgram(shader_program);
        glBindVertexArray(vao);
        // draw vertices from the currently bound VAO with current in-use shader
        glDrawElements(GL_TRIANGLES, sizeof(indices) / sizeof(indices[0]), GL_UNSIGNED_INT, nullptr);

        // free vao
        glBindVertexArray(0);
        // put the stuff we've been drawing onto the display
        glfwSwapBuffers(window);
    }

    glDeleteVertexArrays(1, &vao);
    glDeleteBuffers(1, &vbo);
    glDeleteBuffers(1, &ebo);
    glDeleteProgram(shader_program);

    glfwDestroyWindow(window);
    glfwTerminate();

    return EXIT_SUCCESS;
}
