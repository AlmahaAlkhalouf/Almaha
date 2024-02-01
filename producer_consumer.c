//Producer Consumer module for Group 25
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/moduleparam.h>

#define AUTHOR: "Almaha, Ariadne, Austin, Bao"
MODULE_LICENSE("GPL");

//Passing parameters into module parameter

//Buff size
static int buffSize = 10;
module_param(buffSize, int, 0644);
MODULE_PARM_DESC(buffSize, "The buffer size");

//Number of producers
static int prod = 1;
module_param(prod, int, 0644);
MODULE_PARM_DESC(prod, "The number of producers");


// Number of consumers
static int cons = 10;
module_param(cons,int,0644);
MODULE_PARM_DESC(cons, "The number of consumers");


//UUID for awright
static int uuid = 1000;
module_param(uuid,int,0644);
MODULE_PARM_DESC(cons, "The id of user: Awright");

// Module initializer
int producer_consumer_init(void){
	print(KERN_INFO "Buff size: %d", buffSize);
	return 0;
}

// Module terminator
void producer_consumer_exit(void){
	printk("Mr. Module get out my Kernel!... Please\n");
}

// indicate kernel entry and exit point
module_init(producer_consumer_init); //defines the hello_init to be called at module load
module_exit(producer_consumer_exit); // defines the hello_exit to be called at module unload



