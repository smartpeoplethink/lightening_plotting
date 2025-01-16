import org.jmathplot.gui.*;

/**
 * <p>Copyright : BSD License</p>
 * @author Yann RICHET
 * @version 1.0
 */

public class main {
    public static void main(String[] args) {

        // Build a random 3D data set
        double[][] datas = new double[10][3];

        for (int i = 0; i < datas.length; i++) {
            for (int j = 0; j < datas[0].length; j++) {
                datas[i][j] = Math.random();
            }
        }

        // Build the 3D scatterplot of the datas in a Panel
        Plot3DPanel plot3d = new Plot3DPanel(datas,"datas","SCATTER");

        // Display a Frame containing the plot panel
        new FrameView(plot3d);

    }
}