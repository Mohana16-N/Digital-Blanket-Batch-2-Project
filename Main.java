import java.util.Scanner;

public class Main {
    
    public static String getString(String text, String prefixString, String suffixString) {
        int n = text.length();
        int maxScore = -1;  // Fix: Declare maxScore
        String result = "";

        // Iterate over all possible substrings
        for (int i = 0; i < n; i++) {
            for (int j = i; j < n; j++) {
                String sub = text.substring(i, j + 1);

                // Calculate prefixScore
                int prefixScore = 0;
                for (int k = 1; k <= sub.length(); k++) {
                    if (prefixString.endsWith(sub.substring(0, k))) { // Fix: Correct method name
                        prefixScore = k;
                    }
                }

                // Calculate suffixScore
                int suffixScore = 0;
                for (int k = 1; k <= sub.length(); k++) {
                    if (suffixString.startsWith(sub.substring(sub.length() - k))) { // Fix: Correct method name
                        suffixScore = k;
                    }
                }

                int textScore = prefixScore + suffixScore;

                // Choose the best substring
                if (textScore > maxScore || (textScore == maxScore && sub.compareTo(result) < 0)) { // Fix: Use == for comparison
                    maxScore = textScore;  // Fix: Assign maxScore properly
                    result = sub;
                }
            }
        }

        return result;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String text = sc.next();
        String prefixString = sc.next();
        String suffixString = sc.next();
        System.out.println(getString(text, prefixString, suffixString));
        sc.close();
    }
}
