import java.util.Scanner;

public class Palindrome {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        String string = in.nextLine();
        in.close();

        int[][] memo = new int[string.length()][string.length()];
        System.out.println(lps(string, 0, string.length() - 1, memo));
    }

    /** Returns the length of the Longest Palindromic Substring */
    public static int lps(String s, int i, int j, int[][] memo) {
        if (i == j) {
            return 1;
        }
        if (i > j) {
            return 0;
        }
        if (memo[i][j] == 0) {
            if (s.charAt(i) == s.charAt(j)) {
                memo[i][j] = 2 + lps(s, i + 1, j - 1, memo);
            } else {
                memo[i][j] = Math.max(lps(s, i + 1, j, memo), lps(s, i, j - 1, memo));
            }
        }
        return memo[i][j];
    }
}