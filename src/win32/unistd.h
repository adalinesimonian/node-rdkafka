#ifndef _UNISTD_H
#define _UNISTD_H 1

#include <stdlib.h>
#include <time.h>
#include <chrono>
#include <thread>

/* Visual C++ C runtime is multi-threaded by default;
 * rand is thread safe, unlike other implementations of rand.
 */
#define rand_r(x) rand()

#define usleep(us) std::this_thread::sleep_for(std::chrono::microseconds(us));

#endif
