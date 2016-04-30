import java.io.*;

/**
 * Class containing all the methods required to interpret {@link PrimeGame}
 * output and interact with the user.
 *
 * <p>
 * This subclass contains all the methods necessary for the user to
 * interact with {@link PrimeGame} methods and play the game.
 * @see PrimeGame
 * </p>
 *
 * @author  Joost Bremmer
 * @version 1.0
 * @since   2015
 */
public class PrimeGameCli extends PrimeGame {


  //Subclass properties
  private static BufferedReader stdIn = new BufferedReader(new
                                            InputStreamReader(System.in));

  /** Shows start game and plays first turn */
  public void startGame() {
    System.out.println("Hello,");
    System.out.println("Welcome to \" Prime or not a Prime \"");
    playTurn();
  }

  /**
   * Plays a single turn
   * First prints out number using {@link PrimeGame#getCurrNum}
   * Then takes answer from user using {@ #getAnswer}
   * Checks that answer using {@ #checkAnswer}
   * And finally increments the turn timer.
   * @see PrimeGame#getCurrNum
   * @see #getAnswer
   * @see #checkAnswer
   */
  @Override
  public void playTurn() {
    System.out.println(getCurrNum());
    System.out.println("Is this a prime? y/n");
    boolean answer = false;
    try {
      answer = getAnswer();
    } catch (IOException io) {
      System.out.println(io.getMessage());
    }
    answer = checkAnswer(answer);
    if(answer)
      System.out.println("Correct!");
    else
      System.out.println("Too bad!");
    System.out.println(toString());
    nextTurn();
  }

  /**
   * Makes preperations for the next turn
   * Ressets the next number,
   * Increases the turn timer,
   * Prints stats
   * @see PrimeGame#getNewNumber
   * @see #printStats
   */
  @Override
  public void nextTurn() {
    getNewNumber();
	turns++;
    printStats();
  }

  /**
   * Get some user input on a y/n question
   * @return the user's answer. true for "yes; false for "no"
   */
  public boolean getAnswer() throws IOException {
    boolean answer = false;
    try {
      String input = stdIn.readLine();
      switch (input) {
        case   "y":
        case   "Y":
        case "YES":
        case "yes":
        case "Yes":
          answer = true;
          break;
        case   "n":
        case   "N":
        case  "NO":
        case  "no":
        case  "No":
          answer = false;
          break;
       case "quit":
          System.exit(0);
       default:
          System.out.println("Please answer in yes or no");
          answer =  getAnswer();
      }
    }
    catch(IOException io) {
      System.out.println("Whoops! Looks like something went wrong!");
      System.out.println(io.getMessage());
      System.exit(-1);
    }
    return answer;
  }

  /**
   * Prints the players stats
   * containing score, level, and turns played.
   */
  public void printStats() {
    System.out.println("Level: " + level + " | " +
                       "Score: " + score + " | " +
                       "Turns: " + turns );
  }

  /**
   * The main function which will be fired on running the program
   * @param args String of arguments that are passed from
   *             command-line.
   */
  public static void main (String[] args) {
    PrimeGameCli me = new PrimeGameCli();
    me.startGame();

    while(true) {
      me.playTurn();
    }

  }


}
