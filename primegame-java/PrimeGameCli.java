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
  public int score;
  private int turns;
  private int level;

  /**
   * PrimeGameCli subclass Constructor
   * Sets score to 0;
   * Sets turns to 0;
   * Sets level to 1;
   * @see PrimeGame#Constructor
   */
  public PrimeGameCli() {
    score = 0;
    turns = 0;
    level = 0;
  }

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
    //implement nextTurn() preperation method. 
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
   * Checks if the users guess, gotten from {@link #getAnswer} is correct
   *
   * @param answer user's guess as to whether
   * {@link PrimeGame#getCurrNum } is a prime. 
   * Also handles calls that should happen on
   * a correct answer.
   * 
   * @return true if user correct, false if user is wrong.
   * @see IncreaseMaxRange();
   * @see playTurn();
   */
  public boolean checkAnswer(boolean answer) {
    if (answer == isPrime) {
      System.out.println("Correct!");
      score += getCurrNum();
      increaseMaxRange();
      // implement increaseLevel()
      return true;
    } 
    else {
      System.out.println("Too bad!");
      score = 0;
      return false;
    }
  }

  /**
   * The main function which will be fired on running the program
   * @param args String of arguments that are passed from
   *             command-line.
   */
  public static void main (String[] args) {
    PrimeGameCli me = new PrimeGameCli();
    me.startGame();
    System.out.println(me.toString());
    System.out.println("Score: " + me.score);

  }


}
