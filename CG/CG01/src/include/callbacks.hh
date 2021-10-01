#ifndef __CALLBACKS_HH__
#define __CALLBACKS_HH__

#include <glad/glad.h>
#include <GLFW/glfw3.h>

namespace callbacks
{
    void keyCallback(GLFWwindow *window, int key, int scancode, int action, int mode);
}

#endif // __CALLBACKS_HH__
