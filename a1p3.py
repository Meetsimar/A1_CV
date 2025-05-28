import cv2
import numpy as np
from tkinter import Tk, Button, Label, filedialog, Frame, simpledialog, messagebox
from PIL import Image, ImageTk
import copy
import matplotlib.pyplot as plt

def show_side_by_side(original, modified, title="Preview"):
    original_resized = cv2.resize(original, (300, 300))
    modified_resized = cv2.resize(modified, (300, 300))
    combined = np.hstack((original_resized, modified_resized))

    plt.imshow(cv2.cvtColor(combined, cv2.COLOR_BGR2RGB))
    plt.title(title + "\n[Left: Original | Right: Modified]")
    plt.axis("off")
    plt.show()


# Globals
current_image = None
original_image = None
image_label = None
history = []
operations = []

# === Display Logic ===

def update_display(img_cv):
    global current_image, image_label
    current_image = img_cv.copy()

    display_img = cv2.resize(current_image, (500, 500))
    img_rgb = cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)

    image_label.configure(image=img_tk)
    image_label.image = img_tk

def push_to_history(img):
    history.append(copy.deepcopy(img))

# === Operations ===

def load_image():
    global original_image, current_image, history, operations
    file_path = filedialog.askopenfilename()
    if not file_path: return
    img = cv2.imread(file_path)
    original_image = img.copy()
    current_image = img.copy()
    history = [copy.deepcopy(img)]
    operations.clear()
    update_display(img)

def apply_brightness():
    if current_image is None: return
    value = simpledialog.askinteger("Brightness", "Enter value (-100 to 100):", minvalue=-100, maxvalue=100)
    if value is None: return
    result = cv2.convertScaleAbs(current_image, alpha=1, beta=value)
    show_side_by_side(current_image, result, "Brightness Preview")
    update_display(result)
    push_to_history(result)
    operations.append(f"brightness {value:+}")

def apply_contrast():
    if current_image is None: return
    alpha = simpledialog.askfloat("Contrast", "Enter factor (e.g., 1.5):", minvalue=0.1, maxvalue=5.0)
    if alpha is None: return
    result = cv2.convertScaleAbs(current_image, alpha=alpha, beta=0)
    show_side_by_side(current_image, result, "Contrast Preview")
    update_display(result)
    push_to_history(result)
    operations.append(f"contrast x{alpha:.2f}")


def apply_grayscale():
    if current_image is None: return
    gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
    result = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    show_side_by_side(current_image, result, "Grayscale Preview")
    update_display(result)
    push_to_history(result)
    operations.append("grayscale")


def apply_padding():
    if current_image is None: return
    method = simpledialog.askstring("Padding", "Enter method (constant, reflect, replicate):")
    ratio = simpledialog.askstring("Aspect Ratio", "Enter mode: square / rectangle / ratio (e.g. 4:5):")
    pad = simpledialog.askinteger("Padding Size", "Enter size in px:", minvalue=0, maxvalue=500)
    border_map = {
        "constant": cv2.BORDER_CONSTANT,
        "reflect": cv2.BORDER_REFLECT,
        "replicate": cv2.BORDER_REPLICATE
    }
    border_type = border_map.get(method, cv2.BORDER_REFLECT)
    h, w = current_image.shape[:2]
    top = bottom = left = right = pad

    if ratio == "square":
        if h > w:
            pad_size = (h - w) // 2
            left = right = pad_size
        else:
            pad_size = (w - h) // 2
            top = bottom = pad_size
    elif ":" in ratio:
        try:
            a, b = map(int, ratio.split(":"))
            desired_w = int(h * a / b)
            pad_w = max(0, desired_w - w)
            left = right = pad_w // 2
        except:
            pass

    result = cv2.copyMakeBorder(current_image, top, bottom, left, right, border_type)
    show_side_by_side(current_image, result, "Padding Preview")
    update_display(result)
    push_to_history(result)
    operations.append(f"padded {pad}px with {method} ({ratio})")

def apply_threshold():
    if current_image is None: return
    mode = simpledialog.askstring("Threshold", "Enter mode (binary / inverse):")
    thresh_type = cv2.THRESH_BINARY_INV if mode == "inverse" else cv2.THRESH_BINARY
    gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, thresh_type)
    result = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    show_side_by_side(current_image, result, "Threshold Preview")
    update_display(result)
    push_to_history(result)
    operations.append(f"threshold ({mode})")


def apply_blend():
    if current_image is None: return
    file_path = filedialog.askopenfilename(title="Choose second image")
    if not file_path: return
    alpha = simpledialog.askfloat("Alpha", "Enter alpha (0 to 1):", minvalue=0.0, maxvalue=1.0)
    if alpha is None: return
    img2 = cv2.imread(file_path)
    img2 = cv2.resize(img2, (current_image.shape[1], current_image.shape[0]))
    result = ((1 - alpha) * current_image + alpha * img2).astype(np.uint8)
    show_side_by_side(current_image, result, "Blend Preview")
    update_display(result)
    push_to_history(result)
    operations.append(f"blended with {file_path.split('/')[-1]}, alpha={alpha:.2f}")


def undo_last():
    if len(history) > 1:
        history.pop()
        update_display(history[-1])
        operations.append("undo")
    else:
        messagebox.showinfo("Undo", "Nothing to undo.")

def view_history():
    if not operations:
        messagebox.showinfo("History", "No operations yet.")
        return
    log = "\n".join([f"{i+1}. {op}" for i, op in enumerate(operations)])
    messagebox.showinfo("Operation History", log)

def save_and_exit():
    if current_image is not None:
        filename = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg")])
        if filename:
            cv2.imwrite(filename, current_image)
            view_history()
    root.destroy()

# === GUI Setup ===
root = Tk()
root.title("Full Assignment Photo Editor")

Button(root, text="Upload Image", command=load_image, bg="#3498db", fg="white").pack(pady=10)

image_label = Label(root)
image_label.pack(pady=10)

menu = Frame(root, bg="lightgray")
menu.pack(pady=10)

Button(menu, text="Brightness", command=apply_brightness, width=15).grid(row=0, column=0, padx=5, pady=5)
Button(menu, text="Contrast", command=apply_contrast, width=15).grid(row=0, column=1, padx=5, pady=5)
Button(menu, text="Grayscale", command=apply_grayscale, width=15).grid(row=0, column=2, padx=5, pady=5)
Button(menu, text="Padding", command=apply_padding, width=15).grid(row=0, column=3, padx=5, pady=5)
Button(menu, text="Threshold", command=apply_threshold, width=15).grid(row=1, column=0, padx=5, pady=5)
Button(menu, text="Blend Image", command=apply_blend, width=15).grid(row=1, column=1, padx=5, pady=5)
Button(menu, text="Undo", command=undo_last, width=15).grid(row=1, column=2, padx=5, pady=5)
Button(menu, text="History", command=view_history, width=15).grid(row=1, column=3, padx=5, pady=5)
Button(menu, text="Save & Exit", command=save_and_exit, width=64, bg="#2ecc71", fg="white").grid(row=2, columnspan=4, pady=10)

root.mainloop()
