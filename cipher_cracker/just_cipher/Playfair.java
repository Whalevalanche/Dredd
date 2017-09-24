/**
 * Java program to crack monoalphabetic ciphers.
 *
 * @author Derek S. Prijatelj
 */

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.HashMap;
import java.util.Map;
import java.util.HashSet;
import java.util.stream.IntStream;
import java.util.stream.Collectors;

public class Monoalphabetic{

    private static String decryptCaesar(String cipher, int offset){
        String plainTxt = "";

        for (char ch : cipher.toCharArray()){
            //*
            if (ch >= 'a' && ch <= 'z'){
                plainTxt += (char) (((ch - 'a' + offset) % 26) + 'a');
            } else if (ch >= 'A' && ch <= 'Z'){
                plainTxt += (char) (((ch - 'A' + offset) % 26) + 'A');
            } else{
                plainTxt += ch;
            }
            //*/
        }
        return plainTxt;
    }

    private static String decryptAtbash(String cipher, int offset){
        String alpha = "abcdefghijklmnopqrstuvwxyz";
        String reverseAlpha = new StringBuilder(alpha).reverse().toString();

        char[] alphaNorm = (alpha + alpha.toUpperCase()).toCharArray();
        char[] reverse = (reverseAlpha + reverseAlpha.toUpperCase()
            ).toCharArray();

        Map<Character, Character> map =
            IntStream.range(0, alphaNorm.length).boxed().collect(
            Collectors.toMap(i -> alphaNorm[i], i -> reverse[i]));

        HashMap<Character,Character> reverseMap = new HashMap<>(map);

        String reverseCipher = "";
        for (char ch : cipher.toCharArray()){
            if ((ch >= 'a' && ch <= 'z') || ((ch >= 'A' && ch <= 'Z'))){
                reverseCipher += reverseMap.get(ch);
            } else {
                reverseCipher += ch;
            }
        }

        //System.out.println("\n" + reverseMap.toString() + "\n");
        //System.out.println("\n" + cipher + "\n");
        //System.out.println("\n" + reverseCipher + "\n");

        return decryptCaesar(reverseCipher, offset);
    }

    //private static

    private static boolean test(){
        String alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

        boolean test1 = alpha.equals(
            decryptCaesar("BCDEFGHIJKLMNOPQRSTUVWXYZA", 25));
        System.out.println("Test1 = " + test1);

        boolean test2 = alpha.equals(
            decryptAtbash("ZYXWVUTSRQPONMLKJIHGFEDCBA", 0));
        System.out.println("Test2 = " + test2);

        return test1;
    }

    private static void bruteforce(String cipher){
        String str = "";
        //while(str.size > 0 && str.){
        for(int i = 0; i < 26; i++){
            str = decryptCaesar(cipher, i);
            //str = decryptAtbash(cipher, i);
            System.out.println("Shift = " + i + "\n" + str + "\n");
        }
        //return str;
    }

    public static void main(String[] args){
        //test();
        //*
        String cipher = "";
        for(String str : args)
            cipher += str;

        System.out.println();
        bruteforce(cipher);
        //*/
    }
}
