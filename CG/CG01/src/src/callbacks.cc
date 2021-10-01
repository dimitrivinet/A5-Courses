#include <cstdio>

#include <callbacks.hh>

// Is called whenever a key is pressed/released via GLFW
void callbacks::keyCallback(GLFWwindow *window, int key, int scancode, int action, int mode)
{
    printf("key: %d\n", key);
    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
        glfwSetWindowShouldClose(window, GL_TRUE);
}
