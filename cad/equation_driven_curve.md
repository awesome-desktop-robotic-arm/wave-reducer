**The Strategy:**
Directly entering the equation for the **Outer Profile** into SolidWorks is nearly impossible because calculating the "normal vector" (for the offset) requires a massive equation that exceeds SolidWorks' character limit.

**The Solution:**
Instead, we will define the **Center Path** (the red dashed line from your plot) as the Equation Driven Curve. This equation is much simpler. Then, we will use the standard SolidWorks **"Offset Entities"** command to generate the final profile. This lets the SolidWorks geometry kernel handle the complex vector math for you.

### Step 1: Set up Global Variables

In SolidWorks, go to **Tools \> Equations** and add these global variables (using your values):

  * `"A"` = 25
  * `"B"` = 3
  * `"E"` = 1.2
  * `"Z"` = 10

### Step 2: Create the Equation Driven Curve

1.  Start a new Sketch on the **Top Plane**.
2.  Go to **Tools \> Sketch Entities \> Equation Driven Curve**.
3.  Select **Parametric**.
4.  Enter the following parameters (copy-paste carefully):

**Parameters:**

  * $t_{1}$: `0`
  * $t_{2}$: `2 * pi * "Z"`  *(Note: You might need to type the literal value `62.83` if it complains about the variable in the range field)*.

**Equations:**
SolidWorks uses `sqr()` for square root.

  * **$x_t$**:

    ```text
    ( "E" * cos(t) + sqr( ("A" + "B")^2 - "E"^2 * sin(t)^2 ) ) * cos( t / "Z" )
    ```

  * **$y_t$**:

    ```text
    ( "E" * cos(t) + sqr( ("A" + "B")^2 - "E"^2 * sin(t)^2 ) ) * sin( t / "Z" )
    ```

### Step 3: Create the Gear Profile

1.  Click **OK** to generate the curve. You will see the "flower" shape (the path of the roller centers).
2.  Select the curve you just drew.
3.  Click **Offset Entities** in the sketch toolbar.
4.  Set the offset distance to **`"B"`** (6mm).
5.  Ensure the offset is **Outward** (the larger shape).
6.  Click **OK**.

**Why this is better:**
[cite_start]The "Offset Entities" tool in SolidWorks mathematically calculates the exact **equidistant** (which is what the complex derivation in the paper [cite: 30, 216] was doing manually). By using the CAD tool for the offset, you avoid typing a 500-character equation and ensure perfect geometry.