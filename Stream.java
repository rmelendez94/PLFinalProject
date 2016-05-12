import java.util.*;
import java.util.stream.Collectors;

public class Stream {

    public static List<String> stream1() {
        List<String> myList = Arrays.asList("a1", "a2", "b1", "c2", "c1");

        List<String> myNewList = myList.stream().filter(s -> s.startsWith("c")).map (String::toUpperCase).sorted().collect(Collectors.toList());

        return myNewList;
    }

   /* public static List<String> stream2() {
        List<String> myList = Arrays.asList("a1", "a2", "b1", "c2", "c1");

        List<String> myNewList = myList.stream().filter(s -> s.startsWith("c")).map (String::toUpperCase).sorted().collect(Collectors.toList());

        return myNewList;
    }

    public static List<String> stream3() {
        List<String> myList = Arrays.asList("a1", "a2", "b1", "c2", "c1");

        List<String> myNewList = myList.stream().filter(s -> s.startsWith("c")).map (String::toUpperCase).sorted().collect(Collectors.toList());

        return myNewList;
   }*/
}


