#!/usr/bin/perl

#
# dump symbolic link
#

# usage:
#   sl [options] [files] 

=head

=cut

use strict;
use Getopt::Long;
use Data::Dumper;

my $opts={};
GetOptions( $opts, qw(s q v r h ) ) || die "Error parsing \@ARGV.\n";

my $perldoc = "/usr/bin/perldoc";

if (defined($opts->{h}))
{
  print "
    Usage:
          $0 [options] [files]
          -s    :
          -q    :
          -v    :
          -r    :
          -h    : print this
";
  exit;
}


# Preliminaries.
$|=1;
my $cwd;


# save pwd, if parsing more than one items
if (@ARGV>1)
{
  $cwd = `pwd`;
  if ($?>>8)
  {
    die "cannot find current directory\n";
  }
  chomp($cwd);
}

my @PATH_array = split(/:/, $ENV{PATH});

# do each parameter name
foreach my $name (@ARGV)
{
  my $maxsyslinks=200;
  
  # focus on this name
  #   -e file or directory
  #   -l symbolic link
  if ( !-l $name && !-e $name )
  {
    my $found=0;
    # perhaps it's in the path
    foreach my $p (@PATH_array)
    {
      #  -x filie / directory (execute)
      if (-x "$p/$name")
      {
        $found = 1;
        $name = "$p/$name";
        last;
      }
    }
    
    if (!$found)
    {
      print "file not found : $name\n";
      next;
    }
  }

  # change "//" to "/"
  $name =~ s{/+}{/}g;
  
  # e.g. $name=/cygdrive/j/linux.home/bin/sl.pl
  # e.g. $name=home/MY_USER1/
  my $indent = 0;
  my @indents = ();
  # print "name:[$name]\n" if (!$opts->{q});
  
  my @path = split(m{/}, $name);
  # e.g. @path = ( "", "cygdrive", "j", "linux.home", "bin", "sl.pl", )
  # e.g. @path = ( "home", "MY_USER1", "", )
  # print Dumper(@path) . "\n";

  # make an absolute path related to /.
  if (@path && $path[0] eq '')
  {
    chdir '/';
    shift @path;
    # print "/\n" if (!$opts->{q});
    $indent = 1;
  }
  
  my $elem = '';
  # follow the subdirectories and links, from left to right
  while (@path)
  {
    $elem = shift @path;

    my $pwd_tmp = `pwd`;
    chomp($pwd_tmp);
    # print "pwd=[$pwd_tmp], elem=[$elem]\n";

    if ($elem eq '')
    {
      chdir '/';
      # print "/\n" if (!$opts->{q});
      next;
    }
    elsif ($elem eq '..')
    {
      chdir '..';
      # print "/\n" if (!$opts->{q});
      next;
    }

    
    if (-l $elem)
    {
      my $new = readlink($elem);
      #print "readlink : [$elem] -> [$new]\n";
      # change "//" to "/"
      $new =~ s{/+}{/}g;
      
      if (!$maxsyslinks--)
      {
        print STDERR "too many levels of symbolic link\n";
        exit(1);
      }
      
      print "$pwd_tmp/$elem -> $new\n" if (!$opts->{q});
      # remove "." in head
      # $new =~ s{^\.}{};
      
      # prepend symbolic link to the rest of path
      unshift(@path, split(m{/}, $new));
      # print "debug : new[$new]\n";
      
      #print "================\n";
      #print Dumper(@path);
      #print "================\n";
      #print "pwd=" . `pwd`;
    }
    else
    {
      # elem is NOT a symbolic link
      chdir "$elem";
    }

    # print "\n";
  }
  
  # output the final result
  my $pwd_tmp = `pwd`;
  chomp($pwd_tmp);
  print "$pwd_tmp/$elem\n";
  
}

