import java.util.HashMap;
import java.util.Scanner;

public class Counting {
    public static void main(String[] args) {
        HashMap<Integer, long[]> sub_problems = new HashMap<Integer, long[]>();
        sub_problems.put(0, new long[] { 1, 0 });
        sub_problems.put(1, new long[] { 0, 1 });
        long[] ans;

        Scanner in = new Scanner(System.in);
        int[] problems = new int[in.nextInt()];
        for (int i = 0; i < problems.length; ++i) {
            problems[i] = in.nextInt();
        }
        in.close();

        for (int problem : problems) {
            ans = counts(problem, sub_problems);
            System.out.printf("%s %s\n", ans[0], ans[1]);
        }
    }

    public static long[] counts(int n, HashMap<Integer, long[]> memo) {
        if (n <= 0) {
            return memo.get(0);
        }
        if (!memo.containsKey(n)) {
            memo.put(n, array_sum(counts(n - 1, memo), counts(n - 3, memo)));
        }
        return memo.get(n);
    }

    public static long[] array_sum(long[] arr1, long[] arr2) {
        long[] result = new long[arr1.length];
        for (int i = 0; i < result.length; ++i) {
            result[i] = arr1[i] + arr2[i];
        }
        return result;
    }
}