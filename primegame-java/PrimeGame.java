import java.util.Random;

/**
 * Class containing all the methods required to calculate and check
 * for Prime numbers.
 *
 * <p>
 * This class contains all the methods necessary to primegame
 * But doesn't handle getting in and output from the player.
 * For methods concerning userinteraction check out {@link PrimeGameCli}
 * @see     PrimeGameCli
 * </p>
 *
 * @author  Joost Bremmer
 * @version 1.0
 * @since   2015
 */
public class PrimeGame {

  //Class properties
  private Random              rando;
  private int               current;
  protected boolean         isPrime;
  private int              rangeMax;

  /**
   * PrimeGame constructor:
   * Initializes rangeMax to 10;
   * gets new random number current;
   * checks if it is a prime and stores value
   * in isPrime.
   */
  public PrimeGame() {
    rando    = new Random();
    rangeMax = 10;
    getNewNumber();
    isPrime  = checkPrime(current);
  }

  /**
   * Checks if a number is a prime or not.
   * @param n interger to check against
   * @return whether n was a prime or not as boolean
   *
   */
  public boolean checkPrime(int n) {
    if ( n % 2 == 0) {
      return false;
    } else {
        for (int i=3; i*i <= n; i++) {
          if (n % 2 == 0)
            return false;
        }
      return true;
    }
  }

  /**
   * Returns the current random number
   * @return the current random number
   */
  public int getCurrNum() {
    return current;
  }

  /**
   * Searches for a new random number and puts it into
   * PrimeGame.current
   */
  public void getNewNumber() {
    current = rando.nextInt(rangeMax+1);
  }

  /**
   * Searches for a new random number within the range 0-maxRange
   * and puts it into PrimeGame.current
   *
   * @param maxRange the (inclusive) upper range within to pick
   * a random number
   */
  public void getNewNumber(int maxRange) {
    current = rando.nextInt(maxRange+1);
  }

  /**
   * Return the current upper range {@link #getNewNumber} will pick from.
   *
   * @return inclusive (number will counted amongst possibilities) upper
   *         range from which {@link #getNewNumber} might pick.
   * @see #getNewNumber
   */
  public int getCurrRange() {
    return rangeMax;
  }

  /**
   * Increases max range for {@link #getNewNumber} times 10.
   *
   * @see   #getCurrRange
   * @see   #getNewNumber
   */
   public void increaseMaxRange () {
    rangeMax *= 10;
   }

  /**
   * Increases max range for {@link #getNewNumber} times n.
   *
   * @param n number which the current max Range will be multiplicated by
   * @see   #getCurrRange
   * @see   #getNewNumber
   */
   public void increaseMaxRange (int n) {
    rangeMax *= n;
   }

  /**
   * Returns a string containing all the info of the class
   * for testing purposes.
   * @return all the class's properties in one handy sentence.
   */
  public String toString() {
    String info = "The current number, " + current +
                  " from the range 0-" + rangeMax + " is ";
    if(!isPrime)
      info += "not ";

    info += "a prime!";

    return info;
  }

}

//vim: set tabstop=2 shiftwidth=2 expandtab
