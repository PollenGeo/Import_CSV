import ezomero
from ezomero.rois import Rectangle, Polygon, Ellipse, Line
from omero.gateway import BlitzGateway
import pandas as pd
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def connect(hostname, username, password):
    conn = BlitzGateway(username, password, host=hostname, port=4064, secure=True)
    if not conn.connect():
        raise ConnectionError("Failed to connect to the OMERO server")
    conn.c.enableKeepAlive(60)
    return conn

def list_groups(conn):
    groups = conn.getGroupsMemberOf()
    group_dict = {g.getId(): g.getName() for g in groups}
    group_list_str = "\n".join([f"ID: {g_id} - {name}" for g_id, name in group_dict.items()])
    return group_dict, group_list_str

def change_omero_group(conn, group_id):
    conn.setGroupForSession(group_id)
    print(f"Successfully switched to group with ID {group_id}.")

def add_rois_from_csv(conn, csv_path):
    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        image_id = int(row["image_id"])
        roi_type = row["type"].strip().lower()

        label_text = row.get('text', '')
        label = label_text if pd.notna(label_text) and label_text.strip() != '' else ""

        if roi_type == "rectangle":
            x = int(row["X"])
            y = int(row["Y"])
            width = int(row["Width"])
            height = int(row["Height"])

            roi = Rectangle(
                x=x, y=y, width=width, height=height, z=None,
                label=label
            )

        elif roi_type == "polygon":
            try:
                x_points = list(map(int, row["X_points"].split(',')))
                y_points = list(map(int, row["Y_points"].split(',')))
                if len(x_points) != len(y_points):
                    raise ValueError("Number of X_points and Y_points does not match")

                roi = Polygon(
                    x_points=x_points,
                    y_points=y_points,
                    z=None,
                    label=label
                )
            except Exception as e:
                print(f"Error processing polygon in image {image_id}: {e}")
                continue

        elif roi_type == "ellipse":
            x = int(row["X"])
            y = int(row["Y"])
            width = int(row["Width"])
            height = int(row["Height"])

            roi = Ellipse(
                x=x, y=y, width=width, height=height, z=None,
                label=label
            )

        elif roi_type == "line":
            try:
                x1 = int(row["X1"])
                y1 = int(row["Y1"])
                x2 = int(row["X2"])
                y2 = int(row["Y2"])

                roi = Line(
                    x1=x1, y1=y1, x2=x2, y2=y2, z=None,
                    label=label
                )
            except Exception as e:
                print(f"Error processing line in image {image_id}: {e}")
                continue

        else:
            print(f"ROI type '{roi_type}' not supported. Skipping row.")
            continue

        try:
            ezomero.post_roi(conn, image_id, [roi])
            print(f"ROI of type {roi_type} added to image {image_id}")
        except Exception as e:
            print(f"Error adding ROI to image {image_id}: {e}")

    messagebox.showinfo("Success", "ROIs successfully added to all images.")

def main():
    root = tk.Tk()
    root.withdraw()

    conn = None

    try:
        hostname = simpledialog.askstring("Host", "Host:", initialvalue="xxx")#Put your inicial Host
        username = simpledialog.askstring("Username", "Username:")
        password = simpledialog.askstring("Password", "Password:", show='*')

        if not all([hostname, username, password]):
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        conn = connect(hostname, username, password)

        group_dict, group_list_str = list_groups(conn)

        selected_group_id = simpledialog.askinteger(
            "Select Group",
            f"Available groups:\n{group_list_str}\n\nEnter the ID of the group:"
        )

        if selected_group_id not in group_dict:
            messagebox.showerror("Error", "Invalid group ID.")
            return

        change_omero_group(conn, selected_group_id)

        required_columns = (
            "The CSV file must contain the following columns depending on the ROI type:\n\n"
            "- rectangle: image_id, type, X, Y, Width, Height, text (optional)\n"
            "- polygon: image_id, type, X_points, Y_points, text (optional)\n"
            "- ellipse: image_id, type, X, Y, Width, Height, text (optional)\n"
            "- line: image_id, type, X1, Y1, X2, Y2, text (optional)\n\n"
            "Make sure your file is correctly formatted before continuing."
        )
        messagebox.showinfo("CSV Requirements", required_columns)

        csv_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
        if not csv_path:
            messagebox.showwarning("Input Error", "A CSV file must be selected.")
            return

        add_rois_from_csv(conn, csv_path)

        messagebox.showinfo("Success", "ROIs successfully added to all images.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
