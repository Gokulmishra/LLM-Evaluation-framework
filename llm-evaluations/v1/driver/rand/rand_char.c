#include <linux/module.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/cdev.h>
#include <linux/random.h>

#define DEVICE_NAME "randchar"

static dev_t dev_num;
static struct cdev rand_cdev;

// Open
static int rand_open(struct inode *inode, struct file *file)
{
    pr_info("%s: Device opened\n", DEVICE_NAME);
    return 0;
}

// Release
static int rand_release(struct inode *inode, struct file *file)
{
    pr_info("%s: Device closed\n", DEVICE_NAME);
    return 0;
}

// Read (generate random numbers)
static ssize_t rand_read(struct file *file, char __user *buf, size_t len, loff_t *offset)
{
    char *kbuf;
    int ret;

    kbuf = kmalloc(len, GFP_KERNEL);
    if (!kbuf)
        return -ENOMEM;

    get_random_bytes(kbuf, len);

    ret = copy_to_user(buf, kbuf, len);
    kfree(kbuf);

    if (ret != 0)
        return -EFAULT;

    pr_info("%s: Generated %zu random bytes\n", DEVICE_NAME, len);
    return len;
}

// Write (ignore user data)
static ssize_t rand_write(struct file *file, const char __user *buf, size_t len, loff_t *offset)
{
    pr_info("%s: Discarded %zu bytes written (write not supported)\n", DEVICE_NAME, len);
    return len; // Accept but discard
}

// File operations
static struct file_operations rand_fops = {
    .owner = THIS_MODULE,
    .open = rand_open,
    .release = rand_release,
    .read = rand_read,
    .write = rand_write,
};

// Init
static int __init rand_init(void)
{
    if (alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME) < 0) {
        pr_err("%s: Failed to allocate device number\n", DEVICE_NAME);
        return -1;
    }

    cdev_init(&rand_cdev, &rand_fops);
    if (cdev_add(&rand_cdev, dev_num, 1) < 0) {
        unregister_chrdev_region(dev_num, 1);
        pr_err("%s: Failed to add cdev\n", DEVICE_NAME);
        return -1;
    }

    pr_info("%s: Module loaded, Major=%d Minor=%d\n", DEVICE_NAME, MAJOR(dev_num), MINOR(dev_num));
    return 0;
}

// Exit
static void __exit rand_exit(void)
{
    cdev_del(&rand_cdev);
    unregister_chrdev_region(dev_num, 1);
    pr_info("%s: Module unloaded\n", DEVICE_NAME);
}

module_init(rand_init);
module_exit(rand_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Example Author");
MODULE_DESCRIPTION("Random Number Generator Character Device");

